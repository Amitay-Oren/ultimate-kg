#!/usr/bin/env python3
"""
A2A-Compatible Google ADK Template Copy Script

This script copies the complete A2A-Google ADK template to a target directory,
providing everything needed to start building A2A-compatible agents with Google ADK.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Optional

def print_banner():
    """Print the template copy banner"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                  A2A-Compatible Google ADK Template                  ║
║                                                                      ║
║  Copy this template to start building A2A-compatible AI agents      ║
║  using Google Agent Development Kit with cross-platform             ║
║  interoperability capabilities.                                     ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

def get_template_files() -> List[str]:
    """Get list of all template files to copy"""
    return [
        "CLAUDE.md",
        "README.md",
        ".claude/commands/generate-a2a-google-adk-prp.md",
        ".claude/commands/execute-a2a-google-adk-prp.md",
        "PRPs/templates/prp_a2a_google_adk_base.md",
        "PRPs/ai_docs/a2a_protocol_patterns.md",
        "PRPs/ai_docs/google_adk_integration.md", 
        "PRPs/ai_docs/cross_platform_agent_coordination.md",
        "PRPs/INITIAL.md",
        "examples/basic_a2a_agent/agent.py",
        "examples/basic_a2a_agent/requirements.txt",
        "examples/a2a_server_setup/setup_server.py",
        "examples/a2a_server_setup/docker-compose.yml",
        "examples/cross_platform_delegation/test_delegation.py",
        "examples/cross_platform_delegation/langraph_integration.py",
        "examples/cross_platform_delegation/crewai_integration.py",
        "examples/multi_agent_coordination/coordinator.py",
        "examples/google_cloud_deployment/cloudbuild.yaml",
        "examples/google_cloud_deployment/Dockerfile",
        "examples/a2a_testing_framework/test_compliance.py",
        "config/a2a_server_config.py",
        "config/google_cloud_config.py",
        "config/agent_registry.py",
        "requirements.txt",
        ".env.example",
        ".gitignore"
    ]

def copy_file(src_path: Path, dst_path: Path, template_dir: Path) -> bool:
    """Copy a single file, creating directories as needed"""
    try:
        # Create destination directory if it doesn't exist
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            return True
        else:
            print(f"Warning: Source file not found: {src_path}")
            return False
            
    except Exception as e:
        print(f"Error copying {src_path} to {dst_path}: {e}")
        return False

def copy_template(target_dir: str, template_dir: Optional[str] = None) -> bool:
    """
    Copy the complete A2A-Google ADK template to target directory
    
    Args:
        target_dir: Target directory path
        template_dir: Template source directory (auto-detected if None)
        
    Returns:
        True if successful, False otherwise
    """
    # Get template directory (this script's directory)
    if template_dir is None:
        template_dir = Path(__file__).parent
    else:
        template_dir = Path(template_dir)
    
    target_path = Path(target_dir).resolve()
    
    # Validate target directory
    if target_path.exists() and any(target_path.iterdir()):
        response = input(f"Target directory '{target_path}' is not empty. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Template copy cancelled.")
            return False
    
    # Create target directory
    target_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Copying A2A-Google ADK template to: {target_path}")
    
    # Copy all template files
    files_copied = 0
    files_failed = 0
    
    for file_path in get_template_files():
        src_file = template_dir / file_path
        dst_file = target_path / file_path
        
        if copy_file(src_file, dst_file, template_dir):
            files_copied += 1
            print(f"✓ {file_path}")
        else:
            files_failed += 1
            print(f"✗ {file_path}")
    
    # Copy any additional files that exist
    additional_files = [
        "pyproject.toml",
        "setup.py", 
        "poetry.lock",
        "package.json"
    ]
    
    for file_path in additional_files:
        src_file = template_dir / file_path
        if src_file.exists():
            dst_file = target_path / file_path
            if copy_file(src_file, dst_file, template_dir):
                files_copied += 1
                print(f"✓ {file_path} (additional)")
    
    # Print summary
    print(f"\nTemplate copy completed:")
    print(f"  Files copied: {files_copied}")
    print(f"  Files failed: {files_failed}")
    
    if files_failed > 0:
        print(f"\nWarning: {files_failed} files could not be copied.")
        print("The template should still be functional, but some examples may be missing.")
    
    # Print next steps
    print_next_steps(target_path)
    
    return files_failed == 0

def print_next_steps(target_path: Path):
    """Print next steps after template copy"""
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                            Next Steps                                ║
╚══════════════════════════════════════════════════════════════════════╝

1. Navigate to your new project:
   cd {target_path}

2. Set up your environment:
   cp .env.example .env
   # Edit .env with your Google Cloud and A2A configuration

3. Install dependencies:
   pip install -r requirements.txt

4. Configure Google Cloud authentication:
   gcloud auth application-default login
   export GOOGLE_CLOUD_PROJECT="your-project-id"

5. Start building your A2A-compatible agent:
   # Create your feature requirements
   vim PRPs/INITIAL.md
   
   # Generate implementation plan
   /generate-a2a-google-adk-prp PRPs/INITIAL.md
   
   # Execute the implementation  
   /execute-a2a-google-adk-prp PRPs/your-generated-prp.md

6. Test A2A server setup:
   python config/a2a_server_config.py --validate
   python examples/basic_a2a_agent/agent.py

7. Deploy to Google Cloud:
   gcloud run deploy --source . --region us-central1

📚 Documentation:
   - Read README.md for complete setup instructions
   - Check CLAUDE.md for development patterns
   - See examples/ for working code samples

🔗 A2A Protocol Resources:
   - https://a2a-protocol.org/latest/
   - https://github.com/a2aproject/a2a-python
   - https://github.com/a2aproject/a2a-samples

🚀 Ready to build cross-platform AI agents!
    """)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Copy A2A-Google ADK template to a new project directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python copy_template.py /path/to/my-a2a-project
  python copy_template.py ./my-research-agent
  python copy_template.py ~/projects/a2a-assistant --template-dir ./

This will copy the complete A2A-Google ADK template including:
- A2A protocol implementation patterns
- Google ADK integration examples  
- Cross-platform agent coordination
- Google Cloud deployment configurations
- Testing and validation frameworks
        """
    )
    
    parser.add_argument(
        "target_directory",
        help="Target directory for the new project"
    )
    
    parser.add_argument(
        "--template-dir",
        help="Template source directory (default: script directory)"
    )
    
    parser.add_argument(
        "--list-files", 
        action="store_true",
        help="List all files that would be copied"
    )
    
    parser.add_argument(
        "--no-banner",
        action="store_true", 
        help="Skip printing the banner"
    )
    
    args = parser.parse_args()
    
    if not args.no_banner:
        print_banner()
    
    if args.list_files:
        print("Files that will be copied:")
        for file_path in get_template_files():
            print(f"  {file_path}")
        return
    
    try:
        success = copy_template(args.target_directory, args.template_dir)
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nTemplate copy cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()