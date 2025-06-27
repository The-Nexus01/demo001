"""
Logging configuration for Nexus v2.0
Structured logging with color support
Created by: The Nexus Team
GitHub: https://github.com/The-Nexus-Bot/Nexus-Userbot
License: MIT
"""

import logging
import sys
from pathlib import Path
import os

def setup_logging():
    """Setup logging configuration for Nexus"""
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Log level from environment
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Format for logs
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logs_dir / "nexus.log", encoding="utf-8"),
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("pyrogram").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.session").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.connection").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Nexus v2.0 logging initialized")
    
    return logger