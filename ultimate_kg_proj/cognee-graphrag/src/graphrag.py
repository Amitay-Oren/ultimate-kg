"""Main GraphRAG implementation using Cognee with multi-database architecture."""

import asyncio
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import cognee
from config import setup_all_databases, test_all_connections


@dataclass
class GraphRAGConfig:
    """Configuration for GraphRAG system."""
    
    # Processing settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_concurrent_documents: int = 5
    embedding_batch_size: int = 100
    
    # Search settings
    vector_top_k: int = 10
    graph_depth: int = 2
    combine_results: bool = True
    
    # Database settings
    neo4j_uri: Optional[str] = None
    neo4j_user: Optional[str] = None
    neo4j_password: Optional[str] = None
    lancedb_path: Optional[str] = None
    sqlite_path: Optional[str] = None


class GraphRAG:
    """GraphRAG system using Cognee with Neo4j, LanceDB, and SQLite."""
    
    def __init__(self, config: Optional[GraphRAGConfig] = None):
        self.config = config or GraphRAGConfig()
        self.databases = None
        self._initialized = False
    
    async def initialize(self) -> bool:
        """Initialize the GraphRAG system with all databases."""
        if self._initialized:
            return True
        
        try:
            print("🚀 Initializing GraphRAG system...")
            
            # Setup all database configurations
            self.databases = setup_all_databases()
            
            # Test all connections
            connection_results = test_all_connections()
            
            if not all(connection_results.values()):
                print("⚠️  Some database connections failed")
                return False
            
            # Configure Cognee with our settings
            await self._configure_cognee()
            
            self._initialized = True
            print("✅ GraphRAG system initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize GraphRAG: {e}")
            return False
    
    async def _configure_cognee(self) -> None:
        """Configure Cognee with processing parameters."""
        # Set chunk size and overlap
        cognee.config.set_chunk_size(self.config.chunk_size)
        cognee.config.set_chunk_overlap(self.config.chunk_overlap)
        
        # Additional configuration as needed
        print("🔧 Cognee configuration applied")
    
    async def add_documents(
        self, 
        documents: Union[str, Path, List[Union[str, Path]]]
    ) -> Dict[str, Any]:
        """Add documents to the GraphRAG system."""
        if not self._initialized:
            await self.initialize()
        
        try:
            print("📄 Adding documents to GraphRAG...")
            
            # Convert single document to list
            if isinstance(documents, (str, Path)):
                documents = [documents]
            
            # Add documents to Cognee
            for doc in documents:
                await cognee.add(str(doc))
                print(f"✅ Added: {doc}")
            
            return {"status": "success", "documents_added": len(documents)}
            
        except Exception as e:
            print(f"❌ Error adding documents: {e}")
            return {"status": "error", "error": str(e)}
    
    async def process_documents(self) -> Dict[str, Any]:
        """Process documents to extract entities and relationships."""
        if not self._initialized:
            await self.initialize()
        
        try:
            print("🧠 Processing documents with Cognee...")
            
            # Process documents through Cognee pipeline
            await cognee.cognify()
            
            print("✅ Document processing completed")
            return {"status": "success", "message": "Documents processed successfully"}
            
        except Exception as e:
            print(f"❌ Error processing documents: {e}")
            return {"status": "error", "error": str(e)}
    
    async def search(
        self, 
        query: str,
        search_type: str = "combined",
        top_k: Optional[int] = None
    ) -> Dict[str, Any]:
        """Search across all databases using different strategies."""
        if not self._initialized:
            await self.initialize()
        
        top_k = top_k or self.config.vector_top_k
        
        try:
            print(f"🔍 Searching: '{query}' (type: {search_type})")
            
            if search_type == "vector":
                results = await self._vector_search(query, top_k)
            elif search_type == "graph":
                results = await self._graph_search(query, top_k)
            elif search_type == "combined":
                results = await self._combined_search(query, top_k)
            else:
                raise ValueError(f"Unknown search type: {search_type}")
            
            print(f"✅ Search completed. Found {len(results.get('results', []))} results")
            return results
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return {"status": "error", "error": str(e), "results": []}
    
    async def _vector_search(self, query: str, top_k: int) -> Dict[str, Any]:
        """Perform vector similarity search."""
        try:
            results = await cognee.search(query, search_type="vector")
            
            return {
                "status": "success",
                "search_type": "vector",
                "query": query,
                "results": results[:top_k] if results else []
            }
        except Exception as e:
            return {"status": "error", "error": f"Vector search failed: {e}"}
    
    async def _graph_search(self, query: str, top_k: int) -> Dict[str, Any]:
        """Perform graph-based search."""
        try:
            results = await cognee.search(query, search_type="graph")
            
            return {
                "status": "success",
                "search_type": "graph", 
                "query": query,
                "results": results[:top_k] if results else []
            }
        except Exception as e:
            return {"status": "error", "error": f"Graph search failed: {e}"}
    
    async def _combined_search(self, query: str, top_k: int) -> Dict[str, Any]:
        """Perform combined vector and graph search."""
        try:
            # Get results from both search types
            vector_task = self._vector_search(query, top_k // 2)
            graph_task = self._graph_search(query, top_k // 2)
            
            vector_results, graph_results = await asyncio.gather(
                vector_task, graph_task, return_exceptions=True
            )
            
            # Combine results
            combined_results = []
            
            if isinstance(vector_results, dict) and vector_results.get("results"):
                combined_results.extend(vector_results["results"])
            
            if isinstance(graph_results, dict) and graph_results.get("results"):
                combined_results.extend(graph_results["results"])
            
            # Remove duplicates and limit results
            seen = set()
            unique_results = []
            for result in combined_results:
                result_id = result.get("id", str(result))
                if result_id not in seen:
                    seen.add(result_id)
                    unique_results.append(result)
                    if len(unique_results) >= top_k:
                        break
            
            return {
                "status": "success",
                "search_type": "combined",
                "query": query,
                "results": unique_results,
                "vector_count": len(vector_results.get("results", [])) if isinstance(vector_results, dict) else 0,
                "graph_count": len(graph_results.get("results", [])) if isinstance(graph_results, dict) else 0
            }
            
        except Exception as e:
            return {"status": "error", "error": f"Combined search failed: {e}"}
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics from all databases."""
        if not self._initialized:
            await self.initialize()
        
        stats = {"databases": {}}
        
        try:
            # SQLite stats
            if self.databases and "sqlite" in self.databases:
                sqlite_config = self.databases["sqlite"]
                stats["databases"]["sqlite"] = sqlite_config.get_stats()
            
            # Neo4j stats
            if self.databases and "neo4j" in self.databases:
                neo4j_config = self.databases["neo4j"]
                with neo4j_config.driver.session(database=neo4j_config.database) as session:
                    result = session.run("MATCH (n) RETURN COUNT(n) as node_count")
                    node_count = result.single()["node_count"]
                    
                    result = session.run("MATCH ()-[r]->() RETURN COUNT(r) as rel_count")
                    rel_count = result.single()["rel_count"]
                    
                    stats["databases"]["neo4j"] = {
                        "nodes": node_count,
                        "relationships": rel_count
                    }
            
            # LanceDB stats
            if self.databases and "lancedb" in self.databases:
                lancedb_config = self.databases["lancedb"]
                tables = lancedb_config.list_tables()
                table_info = {}
                for table_name in tables:
                    info = lancedb_config.get_table_info(table_name)
                    if "count" in info:
                        table_info[table_name] = info["count"]
                
                stats["databases"]["lancedb"] = {
                    "tables": len(tables),
                    "table_rows": table_info
                }
            
            stats["status"] = "success"
            
        except Exception as e:
            stats["status"] = "error"
            stats["error"] = str(e)
        
        return stats
    
    async def reset(self) -> Dict[str, Any]:
        """Reset all databases and clear data."""
        if not self._initialized:
            await self.initialize()
        
        try:
            print("🗑️  Resetting GraphRAG system...")
            
            # Use Cognee's prune function to reset memory
            await cognee.prune.prune_memory()
            
            # Also clear our database configurations
            from config import clear_all_databases
            clear_all_databases()
            
            print("✅ GraphRAG system reset completed")
            return {"status": "success", "message": "System reset successfully"}
            
        except Exception as e:
            print(f"❌ Reset error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def close(self) -> None:
        """Close all database connections."""
        if self.databases:
            try:
                if "neo4j" in self.databases:
                    self.databases["neo4j"].close()
                print("✅ Database connections closed")
            except Exception as e:
                print(f"⚠️  Error closing connections: {e}")
        
        self._initialized = False


# Convenience functions
async def create_graphrag(config: Optional[GraphRAGConfig] = None) -> GraphRAG:
    """Create and initialize a GraphRAG instance."""
    graphrag = GraphRAG(config)
    await graphrag.initialize()
    return graphrag


async def quick_start(documents: Union[str, Path, List[Union[str, Path]]]) -> GraphRAG:
    """Quick start: create GraphRAG, add documents, and process them."""
    graphrag = await create_graphrag()
    
    await graphrag.add_documents(documents)
    await graphrag.process_documents()
    
    return graphrag