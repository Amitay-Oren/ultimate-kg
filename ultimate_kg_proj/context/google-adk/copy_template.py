#!/usr/bin/env python3
"""
Google ADK Template Copy Script

This script copies the complete Google Agent Development Kit (ADK) context engineering 
template to a specified target directory, enabling rapid project setup for agent development.

Usage:
    python copy_template.py /path/to/target/directory
    
Example:
    python copy_template.py /home/user/my-adk-project
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

def copy_template(target_dir: str) -> None:
    """
    Copy the Google ADK template to the target directory.
    
    Args:
        target_dir: Path to the target directory where template should be copied
    """
    
    # Get the current directory (where this script is located)
    template_dir = Path(__file__).parent
    target_path = Path(target_dir).resolve()
    
    # Validate target directory
    if target_path.exists():
        response = input(f"Directory '{target_path}' already exists. Continue? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("❌ Copy operation cancelled.")
            return
    
    try:
        # Create target directory if it doesn't exist
        target_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Copying Google ADK template to: {target_path}")
        print("=" * 60)
        
        # Files and directories to copy
        items_to_copy = [
            "CLAUDE.md",
            ".claude/",
            "PRPs/",
            "examples/",
            "README.md"
        ]
        
        # Copy each item
        for item in items_to_copy:
            source_path = template_dir / item
            target_item_path = target_path / item
            
            if source_path.exists():
                if source_path.is_dir():
                    print(f"📂 Copying directory: {item}")
                    shutil.copytree(source_path, target_item_path, dirs_exist_ok=True)
                else:
                    print(f"📄 Copying file: {item}")
                    shutil.copy2(source_path, target_item_path)
            else:
                print(f"⚠️  Warning: {item} not found in template")
        
        # Create additional directories that might be needed
        additional_dirs = [
            "agents",
            "tools", 
            "configs",
            "deployments",
            "tests"
        ]
        
        for dir_name in additional_dirs:
            dir_path = target_path / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True)
                print(f"📁 Created directory: {dir_name}")
        
        # Create basic Python files
        init_files = [
            "agents/__init__.py",
            "tools/__init__.py",
            "configs/__init__.py",
            "tests/__init__.py"
        ]
        
        for init_file in init_files:
            init_path = target_path / init_file
            if not init_path.exists():
                init_path.write_text("# Google ADK Agent Development\n")
                print(f"📄 Created: {init_file}")
        
        # Create environment template
        env_example_path = target_path / ".env.example"
        if not env_example_path.exists():
            env_content = """# Google ADK Configuration
ADK_MODEL=gemini-2.0-flash
GOOGLE_CLOUD_PROJECT=your-project-id
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Optional: Alternative model providers
# OPENAI_API_KEY=your-openai-key
# ANTHROPIC_API_KEY=your-anthropic-key
"""
            env_example_path.write_text(env_content)
            print("📄 Created: .env.example")
        
        # Create basic requirements.txt
        requirements_path = target_path / "requirements.txt"
        if not requirements_path.exists():
            requirements_content = """# Google Agent Development Kit
google-adk

# Environment management
python-dotenv

# Optional: Development tools
pytest
black
isort
mypy

# Optional: Alternative model providers
# openai
# anthropic
"""
            requirements_path.write_text(requirements_content)
            print("📄 Created: requirements.txt")
        
        print("=" * 60)
        print("✅ Google ADK template copied successfully!")
        print()
        print("🚀 Next Steps:")
        print("1. Navigate to your project directory:")
        print(f"   cd {target_path}")
        print()
        print("2. Set up Python environment:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("   pip install -r requirements.txt")
        print()
        print("3. Configure environment:")
        print("   cp .env.example .env")
        print("   # Edit .env with your Google Cloud configuration")
        print()
        print("4. Define your agent requirements:")
        print("   # Edit PRPs/INITIAL.md with your specific agent needs")
        print()
        print("5. Generate and execute PRP:")
        print("   /generate-google-adk-prp PRPs/INITIAL.md")
        print("   /execute-google-adk-prp PRPs/generated-prp.md")
        print()
        print("📚 Documentation: Check README.md for detailed instructions")
        
    except Exception as e:
        print(f"❌ Error copying template: {e}")
        sys.exit(1)

def main():
    """Main function to handle command line arguments and execute copy operation."""
    
    parser = argparse.ArgumentParser(
        description="Copy Google ADK context engineering template to target directory",
        epilog="""
Examples:
  python copy_template.py /home/user/my-adk-project
  python copy_template.py C:\\Users\\user\\my-adk-project
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "target_directory",
        help="Target directory where the template will be copied"
    )
    
    parser.add_argument(
        "--version",
        action="version", 
        version="Google ADK Template Copy Script v1.0"
    )
    
    # Show usage if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        print()
        print("📖 Usage Examples:")
        print("  python copy_template.py /path/to/my-agent-project")
        print("  python copy_template.py C:\\path\\to\\my-agent-project")
        return
    
    args = parser.parse_args()
    
    # Execute copy operation
    copy_template(args.target_directory)

if __name__ == "__main__":
    main()