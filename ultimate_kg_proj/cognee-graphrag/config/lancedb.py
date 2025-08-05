"""LanceDB configuration and connection management for GraphRAG."""

import os
from typing import Optional, Dict, Any, List
from pathlib import Path
import lancedb
from dotenv import load_dotenv

load_dotenv()


class LanceDBConfig:
    """LanceDB configuration and connection management."""
    
    def __init__(
        self,
        path: Optional[str] = None,
        table_name: Optional[str] = None,
    ):
        self.path = path or os.getenv("LANCEDB_PATH", "./lancedb_data")
        self.table_name = table_name or os.getenv("LANCEDB_TABLE_NAME", "documents")
        self._connection = None
        
        # Ensure directory exists
        Path(self.path).mkdir(parents=True, exist_ok=True)
    
    @property
    def connection(self):
        """Get or create LanceDB connection."""
        if self._connection is None:
            self._connection = lancedb.connect(self.path)
        return self._connection
    
    def test_connection(self) -> bool:
        """Test the LanceDB connection."""
        try:
            # Try to list tables
            tables = self.connection.table_names()
            print(f"LanceDB connection successful. Found {len(tables)} tables.")
            return True
        except Exception as e:
            print(f"LanceDB connection test failed: {e}")
            return False
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration dictionary for Cognee."""
        return {
            "vector_db_provider": "lancedb",
            "lancedb_path": self.path,
            "lancedb_table_name": self.table_name,
        }
    
    def list_tables(self) -> List[str]:
        """List all tables in LanceDB."""
        try:
            return self.connection.table_names()
        except Exception as e:
            print(f"Error listing tables: {e}")
            return []
    
    def get_table_info(self, table_name: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a specific table."""
        table_name = table_name or self.table_name
        try:
            if table_name in self.connection.table_names():
                table = self.connection.open_table(table_name)
                return {
                    "name": table_name,
                    "schema": table.schema,
                    "count": table.count_rows(),
                    "version": table.version,
                }
            else:
                return {"error": f"Table {table_name} not found"}
        except Exception as e:
            return {"error": f"Error getting table info: {e}"}
    
    def create_sample_table(self) -> None:
        """Create a sample table for testing."""
        try:
            import pyarrow as pa
            
            # Sample data schema for document embeddings
            schema = pa.schema([
                pa.field("id", pa.string()),
                pa.field("text", pa.string()),
                pa.field("embedding", pa.list_(pa.float32())),
                pa.field("metadata", pa.string()),
                pa.field("timestamp", pa.timestamp("s")),
            ])
            
            # Create empty table with schema
            self.connection.create_table(
                self.table_name,
                schema=schema,
                mode="overwrite"
            )
            print(f"✅ Created sample table: {self.table_name}")
            
        except Exception as e:
            print(f"❌ Error creating sample table: {e}")
    
    def clear_table(self, table_name: Optional[str] = None) -> None:
        """Clear all data from a specific table."""
        table_name = table_name or self.table_name
        try:
            if table_name in self.connection.table_names():
                table = self.connection.open_table(table_name)
                table.delete("true")  # Delete all rows
                print(f"✅ Cleared table: {table_name}")
            else:
                print(f"⚠️  Table {table_name} not found")
        except Exception as e:
            print(f"❌ Error clearing table: {e}")
    
    def clear_database(self) -> None:
        """Clear all tables in LanceDB."""
        try:
            tables = self.list_tables()
            for table_name in tables:
                self.clear_table(table_name)
            print("✅ LanceDB database cleared")
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
    
    def optimize_table(self, table_name: Optional[str] = None) -> None:
        """Optimize table for better performance."""
        table_name = table_name or self.table_name
        try:
            if table_name in self.connection.table_names():
                table = self.connection.open_table(table_name)
                table.optimize()
                print(f"✅ Optimized table: {table_name}")
            else:
                print(f"⚠️  Table {table_name} not found")
        except Exception as e:
            print(f"❌ Error optimizing table: {e}")


def get_lancedb_config() -> LanceDBConfig:
    """Get configured LanceDB instance."""
    return LanceDBConfig()


def setup_cognee_lancedb():
    """Configure Cognee to use LanceDB."""
    import cognee
    
    config = get_lancedb_config()
    cognee.config.set_vector_db_config(config.get_config_dict())
    
    # Test connection
    if config.test_connection():
        print("✅ LanceDB connection successful")
        
        # Create sample table if it doesn't exist
        if config.table_name not in config.list_tables():
            config.create_sample_table()
    else:
        print("❌ LanceDB connection failed")
        
    return config