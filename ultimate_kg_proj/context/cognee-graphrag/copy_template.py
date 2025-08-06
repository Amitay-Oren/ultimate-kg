#!/usr/bin/env python3
"""
Template copy utility for Cognee GraphRAG use case.

This script copies the Cognee GraphRAG template to a new project directory,
with customization options for project name, databases, and configuration.
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import Dict, Any
import uuid


def generate_project_id() -> str:
    """Generate a unique project identifier."""
    return str(uuid.uuid4())[:8]


def get_template_variables(project_name: str, target_dir: Path) -> Dict[str, str]:
    """Get template variables for customization."""
    
    variables = {
        "PROJECT_NAME": project_name,
        "PROJECT_NAME_UNDERSCORE": project_name.replace("-", "_").replace(" ", "_"),
        "PROJECT_ID": generate_project_id(),
        "TARGET_DIR": str(target_dir),
        "TEMPLATE_VERSION": "0.1.0",
    }
    
    # Database configuration prompts
    print(f"\n🔧 Configuring databases for '{project_name}'...")
    
    # Neo4j configuration
    neo4j_uri = input("Neo4j URI (default: bolt://localhost:7687): ").strip()
    variables["NEO4J_URI"] = neo4j_uri or "bolt://localhost:7687"
    
    neo4j_user = input("Neo4j username (default: neo4j): ").strip()
    variables["NEO4J_USER"] = neo4j_user or "neo4j"
    
    neo4j_password = input("Neo4j password (default: password123): ").strip()
    variables["NEO4J_PASSWORD"] = neo4j_password or "password123"
    
    # LanceDB configuration
    lancedb_path = input("LanceDB path (default: ./lancedb_data): ").strip()
    variables["LANCEDB_PATH"] = lancedb_path or "./lancedb_data"
    
    # SQLite configuration
    sqlite_path = input("SQLite path (default: ./cognee.db): ").strip()
    variables["SQLITE_PATH"] = sqlite_path or "./cognee.db"
    
    # OpenAI API Key prompt
    openai_key = input("OpenAI API Key (leave empty to set later): ").strip()
    variables["OPENAI_API_KEY"] = openai_key or "your_openai_key_here"
    
    return variables


def customize_file_content(content: str, variables: Dict[str, str]) -> str:
    """Customize file content with template variables."""
    
    for key, value in variables.items():
        # Replace template placeholders
        content = content.replace(f"{{{{{key}}}}}", value)
        content = content.replace(f"%%{key}%%", value)
        
        # Handle specific replacements
        if key == "PROJECT_NAME":
            # Update project names in various formats
            content = content.replace("cognee-graphrag", value)
            content = content.replace("Cognee GraphRAG", value.replace("-", " ").title())
        
        elif key == "PROJECT_NAME_UNDERSCORE":
            # Update Python module names
            content = content.replace("cognee_graphrag", value)
    
    return content


def copy_template(source_dir: Path, target_dir: Path, variables: Dict[str, str]):
    """Copy template files with customization."""
    
    # Files to skip during copy
    skip_files = {
        "__pycache__",
        ".git",
        ".pytest_cache",
        "*.pyc",
        ".DS_Store",
        "copy_template.py"  # Don't copy the template script itself
    }
    
    # Files that need content customization
    customize_extensions = {".py", ".md", ".toml", ".json", ".env", ".txt", ".yml", ".yaml"}
    
    def should_skip(path: Path) -> bool:
        """Check if path should be skipped."""
        for skip_pattern in skip_files:
            if skip_pattern in str(path):
                return True
        return False
    
    def copy_file(src: Path, dst: Path):
        """Copy a single file with optional customization."""
        if should_skip(src):
            return
        
        # Ensure destination directory exists
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file needs content customization
        if src.suffix in customize_extensions:
            try:
                content = src.read_text(encoding='utf-8')
                customized_content = customize_file_content(content, variables)
                dst.write_text(customized_content, encoding='utf-8')
                print(f"   📝 Customized: {dst.relative_to(target_dir)}")
            except Exception as e:
                print(f"   ⚠️  Error customizing {src}: {e}")
                # Fall back to regular copy
                shutil.copy2(src, dst)
                print(f"   📄 Copied: {dst.relative_to(target_dir)}")
        else:
            # Regular file copy
            shutil.copy2(src, dst)
            print(f"   📄 Copied: {dst.relative_to(target_dir)}")
    
    # Walk through source directory
    for src_path in source_dir.rglob("*"):
        if src_path.is_file() and not should_skip(src_path):
            # Calculate relative path and destination
            rel_path = src_path.relative_to(source_dir)
            dst_path = target_dir / rel_path
            
            copy_file(src_path, dst_path)


def create_project_readme(target_dir: Path, variables: Dict[str, str]):
    """Create a customized project README."""
    
    readme_content = f"""# {variables['PROJECT_NAME'].title()}

A GraphRAG implementation using Cognee with Neo4j, LanceDB, and SQLite.

## 🚀 Quick Setup

1. **Install dependencies:**
   ```bash
   cd {variables['PROJECT_NAME']}
   uv sync
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start databases:**
   ```bash
   # Neo4j
   docker run -d --name neo4j-{variables['PROJECT_ID']} \\
     -p 7474:7474 -p 7687:7687 \\
     -e NEO4J_AUTH={variables['NEO4J_USER']}/{variables['NEO4J_PASSWORD']} \\
     neo4j:latest
   ```

4. **Test setup:**
   ```bash
   uv run examples/basic_setup.py
   ```

5. **Process documents:**
   ```bash
   uv run examples/document_processing.py
   ```

## 📊 Database Configuration

- **Neo4j**: {variables['NEO4J_URI']}
- **LanceDB**: {variables['LANCEDB_PATH']}
- **SQLite**: {variables['SQLITE_PATH']}

## 🔧 Next Steps

1. Add your documents to process
2. Configure OpenAI API key for embeddings
3. Set up Cognee MCP server for Claude Code integration
4. Customize the GraphRAG configuration

Generated from Cognee GraphRAG template v{variables['TEMPLATE_VERSION']}
Project ID: {variables['PROJECT_ID']}
"""
    
    readme_path = target_dir / "PROJECT_README.md"
    readme_path.write_text(readme_content)
    print(f"   📚 Created: PROJECT_README.md")


def main():
    """Main template copy function."""
    parser = argparse.ArgumentParser(
        description="Copy Cognee GraphRAG template to new project"
    )
    parser.add_argument(
        "project_name",
        help="Name of the new project"
    )
    parser.add_argument(
        "target_directory",
        nargs="?",
        help="Target directory (default: ./PROJECT_NAME)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive configuration mode"
    )
    
    args = parser.parse_args()
    
    # Get template directory (current directory)
    template_dir = Path(__file__).parent
    
    # Determine target directory
    if args.target_directory:
        target_dir = Path(args.target_directory).resolve()
    else:
        target_dir = Path.cwd() / args.project_name
    
    print(f"📦 Copying Cognee GraphRAG Template")
    print(f"   Source: {template_dir}")
    print(f"   Target: {target_dir}")
    print(f"   Project: {args.project_name}")
    
    # Check if target exists
    if target_dir.exists():
        print(f"⚠️  Target directory already exists: {target_dir}")
        overwrite = input("Continue and overwrite? (yes/no): ").lower().strip()
        if overwrite != "yes":
            print("❌ Copy cancelled")
            return
    
    # Get template variables
    if args.interactive:
        variables = get_template_variables(args.project_name, target_dir)
    else:
        variables = {
            "PROJECT_NAME": args.project_name,
            "PROJECT_NAME_UNDERSCORE": args.project_name.replace("-", "_").replace(" ", "_"),
            "PROJECT_ID": generate_project_id(),
            "TARGET_DIR": str(target_dir),
            "TEMPLATE_VERSION": "0.1.0",
            "NEO4J_URI": "bolt://localhost:7687",
            "NEO4J_USER": "neo4j", 
            "NEO4J_PASSWORD": "password123",
            "LANCEDB_PATH": "./lancedb_data",
            "SQLITE_PATH": "./cognee.db",
            "OPENAI_API_KEY": "your_openai_key_here",
        }
    
    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy template files
    print(f"\n📁 Copying template files...")
    copy_template(template_dir, target_dir, variables)
    
    # Create project-specific README
    print(f"\n📚 Creating project documentation...")
    create_project_readme(target_dir, variables)
    
    print(f"\n✅ Template copied successfully!")
    print(f"\n🚀 Next steps:")
    print(f"   cd {target_dir}")
    print(f"   uv sync")
    print(f"   cp .env.example .env")
    print(f"   # Edit .env with your configuration")
    print(f"   uv run examples/basic_setup.py")
    
    if variables.get("OPENAI_API_KEY") == "your_openai_key_here":
        print(f"\n⚠️  Don't forget to set your OpenAI API key in .env!")


if __name__ == "__main__":
    main()