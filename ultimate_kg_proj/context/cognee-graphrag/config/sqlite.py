"""SQLite configuration and connection management for GraphRAG."""

import os
import sqlite3
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class SQLiteConfig:
    """SQLite database configuration and connection management."""
    
    def __init__(self, path: Optional[str] = None):
        self.path = path or os.getenv("SQLITE_PATH", "./cognee.db")
        
        # Ensure directory exists
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get SQLite connection with optimized settings."""
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        
        # Optimize SQLite for our use case
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute("PRAGMA cache_size = 10000")
        conn.execute("PRAGMA temp_store = memory")
        
        return conn
    
    def test_connection(self) -> bool:
        """Test the SQLite connection."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("SELECT 1")
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            print(f"SQLite connection test failed: {e}")
            return False
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration dictionary for Cognee."""
        return {
            "relational_db_provider": "sqlite",
            "sqlite_path": self.path,
        }
    
    def create_tables(self) -> None:
        """Create necessary tables for GraphRAG metadata."""
        schema_sql = """
        -- Documents table
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            filepath TEXT,
            content_type TEXT,
            size_bytes INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed_at TIMESTAMP,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'error')),
            error_message TEXT,
            metadata TEXT -- JSON metadata
        );
        
        -- Document chunks table
        CREATE TABLE IF NOT EXISTS document_chunks (
            id TEXT PRIMARY KEY,
            document_id TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            token_count INTEGER,
            embedding_id TEXT, -- Reference to vector DB
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
        );
        
        -- Entities extracted from documents
        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            document_id TEXT NOT NULL,
            chunk_id TEXT,
            confidence_score REAL,
            neo4j_id TEXT, -- Reference to Neo4j node
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE,
            FOREIGN KEY (chunk_id) REFERENCES document_chunks (id) ON DELETE SET NULL
        );
        
        -- Relationships between entities
        CREATE TABLE IF NOT EXISTS relationships (
            id TEXT PRIMARY KEY,
            source_entity_id TEXT NOT NULL,
            target_entity_id TEXT NOT NULL,
            relationship_type TEXT NOT NULL,
            description TEXT,
            confidence_score REAL,
            document_id TEXT NOT NULL,
            neo4j_id TEXT, -- Reference to Neo4j relationship
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_entity_id) REFERENCES entities (id) ON DELETE CASCADE,
            FOREIGN KEY (target_entity_id) REFERENCES entities (id) ON DELETE CASCADE,
            FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
        );
        
        -- Processing jobs and status
        CREATE TABLE IF NOT EXISTS processing_jobs (
            id TEXT PRIMARY KEY,
            job_type TEXT NOT NULL,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'error')),
            input_data TEXT, -- JSON input parameters
            output_data TEXT, -- JSON output results
            error_message TEXT,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Configuration and settings
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Search and query logs
        CREATE TABLE IF NOT EXISTS query_logs (
            id TEXT PRIMARY KEY,
            query_text TEXT NOT NULL,
            query_type TEXT NOT NULL, -- 'vector', 'graph', 'combined'
            results_count INTEGER,
            execution_time_ms INTEGER,
            user_id TEXT,
            session_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        with self.get_connection() as conn:
            conn.executescript(schema_sql)
            print("✅ SQLite tables created successfully")
    
    def create_indexes(self) -> None:
        """Create indexes for better performance."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_documents_status ON documents (status)",
            "CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents (created_at)",
            "CREATE INDEX IF NOT EXISTS idx_document_chunks_document_id ON document_chunks (document_id)",
            "CREATE INDEX IF NOT EXISTS idx_entities_document_id ON entities (document_id)",
            "CREATE INDEX IF NOT EXISTS idx_entities_type ON entities (type)",
            "CREATE INDEX IF NOT EXISTS idx_entities_name ON entities (name)",
            "CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships (source_entity_id)",
            "CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships (target_entity_id)",
            "CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships (relationship_type)",
            "CREATE INDEX IF NOT EXISTS idx_processing_jobs_status ON processing_jobs (status)",
            "CREATE INDEX IF NOT EXISTS idx_query_logs_created_at ON query_logs (created_at)",
        ]
        
        with self.get_connection() as conn:
            for index in indexes:
                try:
                    conn.execute(index)
                except Exception as e:
                    print(f"Index creation failed: {e}")
            print("✅ SQLite indexes created successfully")
    
    def get_table_info(self) -> Dict[str, Any]:
        """Get information about all tables."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT name, sql FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)
            tables = cursor.fetchall()
            
            table_info = {}
            for table in tables:
                table_name = table['name']
                cursor = conn.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = cursor.fetchone()['count']
                table_info[table_name] = {
                    'sql': table['sql'],
                    'row_count': count
                }
            
            return table_info
    
    def clear_database(self) -> None:
        """Clear all data from the SQLite database."""
        tables = [
            'query_logs', 'processing_jobs', 'relationships', 
            'entities', 'document_chunks', 'documents', 'config'
        ]
        
        with self.get_connection() as conn:
            for table in tables:
                try:
                    conn.execute(f"DELETE FROM {table}")
                    print(f"✅ Cleared table: {table}")
                except Exception as e:
                    print(f"❌ Error clearing table {table}: {e}")
            conn.commit()
            print("✅ SQLite database cleared")
    
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        with self.get_connection() as conn:
            stats = {}
            tables = ['documents', 'document_chunks', 'entities', 'relationships', 'processing_jobs']
            
            for table in tables:
                try:
                    cursor = conn.execute(f"SELECT COUNT(*) as count FROM {table}")
                    stats[table] = cursor.fetchone()['count']
                except Exception:
                    stats[table] = 0
            
            return stats


def get_sqlite_config() -> SQLiteConfig:
    """Get configured SQLite instance."""
    return SQLiteConfig()


def setup_cognee_sqlite():
    """Configure Cognee to use SQLite."""
    import cognee
    
    config = get_sqlite_config()
    cognee.config.set_relational_db_config(config.get_config_dict())
    
    # Test connection and setup schema
    if config.test_connection():
        print("✅ SQLite connection successful")
        config.create_tables()
        config.create_indexes()
    else:
        print("❌ SQLite connection failed")
        
    return config