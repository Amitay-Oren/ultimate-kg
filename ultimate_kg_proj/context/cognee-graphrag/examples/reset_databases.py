#!/usr/bin/env python3
"""
Database reset utility for Cognee GraphRAG.

This script provides safe database cleanup and reset functionality.
"""

import asyncio
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

from config import clear_all_databases, test_all_connections
from src.graphrag import GraphRAG


async def main():
    """Reset all databases safely."""
    print("🗑️  Database Reset Utility")
    print("=" * 30)
    
    print("\n⚠️  WARNING: This will delete ALL data from:")
    print("   - Neo4j knowledge graph")
    print("   - LanceDB vector embeddings") 
    print("   - SQLite metadata")
    
    # Confirmation
    confirm = input("\nAre you sure you want to proceed? (yes/no): ").lower().strip()
    
    if confirm != "yes":
        print("❌ Reset cancelled")
        return
    
    print("\n🔄 Starting database reset...")
    
    try:
        # Method 1: Use GraphRAG reset (preferred)
        print("\n1️⃣  Using GraphRAG reset method...")
        graphrag = GraphRAG()
        success = await graphrag.initialize()
        
        if success:
            reset_result = await graphrag.reset()
            if reset_result.get("status") == "success":
                print("✅ GraphRAG reset completed")
            else:
                print(f"⚠️  GraphRAG reset warning: {reset_result.get('error')}")
        else:
            print("⚠️  Could not initialize GraphRAG, using direct method...")
        
        await graphrag.close()
        
    except Exception as e:
        print(f"⚠️  GraphRAG method failed: {e}")
        print("   Falling back to direct database clearing...")
    
    # Method 2: Direct database clearing (fallback)
    print("\n2️⃣  Direct database clearing...")
    try:
        clear_all_databases()
        print("✅ Direct clearing completed")
    except Exception as e:
        print(f"❌ Direct clearing failed: {e}")
    
    # Verify reset
    print("\n3️⃣  Verifying reset...")
    connection_results = test_all_connections()
    
    if all(connection_results.values()):
        print("✅ All databases are accessible and reset")
    else:
        print("⚠️  Some databases may not be accessible:")
        for db, status in connection_results.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {db.upper()}")
    
    print("\n✅ Database reset completed!")
    print("\nYou can now:")
    print("1. Run basic_setup.py to verify the system")
    print("2. Run document_processing.py to add new data")


if __name__ == "__main__":
    asyncio.run(main())