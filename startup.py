#!/usr/bin/env python3
"""
Nexus v2.0 Startup Script
Verifies environment and starts the bot
"""
import os
import sys
import logging
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import pyrogram
        import tgcrypto
        import requests
        import aiohttp
        import psutil
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['API_ID', 'API_HASH', 'SESSION_STRING']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\nRequired variables:")
        print("- API_ID: Get from https://my.telegram.org")
        print("- API_HASH: Get from https://my.telegram.org")
        print("- SESSION_STRING: Generate using 'python generate_session.py'")
        return False
    
    print("✅ Environment variables configured")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'downloads', 'assets']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")

def main():
    """Main startup function"""
    print("🚀 Nexus v2.0 - Starting up...")
    print("=" * 50)
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
        
    if not check_dependencies():
        sys.exit(1)
        
    if not check_environment():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("=" * 50)
    print("✅ All checks passed! Starting Nexus...")
    
    # Import and run main application
    try:
        from main import main as run_main
        import asyncio
        asyncio.run(run_main())
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()