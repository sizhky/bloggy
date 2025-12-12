from pathlib import Path
import sys
import os
from .config import get_config, reload_config

# Import app at module level, but config will be initialized before it's used
from .core import app

def cli():
    """CLI entry point for bloggy command
    
    Usage:
        bloggy [directory]                    # Run locally on 127.0.0.1:5001
        bloggy [directory] --host 0.0.0.0     # Run on all interfaces
        
    Environment variables:
        BLOGGY_ROOT: Path to markdown files
        BLOGGY_HOST: Server host (default: 127.0.0.1)
        BLOGGY_PORT: Server port (default: 5001)
        
    Configuration file:
        Create a .bloggy file (TOML format) in your blog directory
    """
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Bloggy server')
    parser.add_argument('directory', nargs='?', help='Path to markdown files directory')
    parser.add_argument('--host', help='Server host (default: 127.0.0.1, use 0.0.0.0 for all interfaces)')
    parser.add_argument('--port', type=int, help='Server port (default: 5001)')
    parser.add_argument('--no-reload', action='store_true', help='Disable auto-reload')
    
    args = parser.parse_args()
    
    # Set root folder from arguments or environment
    if args.directory:
        root = Path(args.directory).resolve()
        if not root.exists():
            print(f"Error: Directory {root} does not exist")
            sys.exit(1)
        os.environ['BLOGGY_ROOT'] = str(root)
    
    # Initialize or reload config to pick up .bloggy file
    # This ensures .bloggy file is loaded and config is refreshed
    config = reload_config() if args.directory else get_config()
    
    # Get host and port from arguments, config, or use defaults
    host = args.host or config.get_host()
    port = args.port or config.get_port()
    reload = not args.no_reload
    
    print(f"Starting Bloggy server...")
    print(f"Blog root: {config.get_root_folder()}")
    print(f"Blog title: {config.get_blog_title()}")
    print(f"Serving at: http://{host}:{port}")
    if host == '0.0.0.0':
        print(f"Server accessible from network at: http://<your-ip>:{port}")
    
    uvicorn.run("bloggy.main:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    cli()