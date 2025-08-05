"""Neo4j configuration and connection management for GraphRAG."""

import os
from typing import Optional, Dict, Any
from neo4j import GraphDatabase, Driver
from dotenv import load_dotenv

load_dotenv()


class Neo4jConfig:
    """Neo4j database configuration and connection management."""
    
    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
    ):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password123")
        self.database = database or os.getenv("NEO4J_DATABASE", "neo4j")
        self._driver: Optional[Driver] = None
    
    @property
    def driver(self) -> Driver:
        """Get or create Neo4j driver."""
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
        return self._driver
    
    def close(self) -> None:
        """Close the Neo4j driver connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def test_connection(self) -> bool:
        """Test the Neo4j connection."""
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run("RETURN 1")
                return result.single() is not None
        except Exception as e:
            print(f"Neo4j connection test failed: {e}")
            return False
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration dictionary for Cognee."""
        return {
            "graph_db_provider": "neo4j",
            "neo4j_uri": self.uri,
            "neo4j_user": self.user,
            "neo4j_password": self.password,
            "neo4j_database": self.database,
        }
    
    def setup_indexes(self) -> None:
        """Create recommended indexes for GraphRAG performance."""
        indexes = [
            "CREATE INDEX entity_name_idx IF NOT EXISTS FOR (e:Entity) ON (e.name)",
            "CREATE INDEX entity_type_idx IF NOT EXISTS FOR (e:Entity) ON (e.type)",
            "CREATE INDEX document_id_idx IF NOT EXISTS FOR (d:Document) ON (d.id)",
            "CREATE INDEX chunk_id_idx IF NOT EXISTS FOR (c:Chunk) ON (c.id)",
            "CREATE CONSTRAINT entity_id_unique IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT document_id_unique IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
        ]
        
        with self.driver.session(database=self.database) as session:
            for index in indexes:
                try:
                    session.run(index)
                    print(f"Created index: {index.split('FOR')[0].strip()}")
                except Exception as e:
                    print(f"Index creation failed: {e}")
    
    def clear_database(self) -> None:
        """Clear all data from the Neo4j database."""
        with self.driver.session(database=self.database) as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Neo4j database cleared")


def get_neo4j_config() -> Neo4jConfig:
    """Get configured Neo4j instance."""
    return Neo4jConfig()


def setup_cognee_neo4j():
    """Configure Cognee to use Neo4j."""
    import cognee
    
    config = get_neo4j_config()
    cognee.config.set_graph_db_config(config.get_config_dict())
    
    # Test connection and setup indexes
    if config.test_connection():
        print("✅ Neo4j connection successful")
        config.setup_indexes()
    else:
        print("❌ Neo4j connection failed")
        
    return config