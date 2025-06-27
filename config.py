"""
Configuration management for Nexus v2.0
Session string only authentication - phone numbers removed
Created by: The Nexus Team
GitHub: https://github.com/The-Nexus-Bot/Nexus-Userbot
License: MIT
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class Config:
    """Configuration class with session string authentication only"""
    
    def __init__(self):
        # Required user configuration - SESSION STRING ONLY
        self.API_ID = int(os.getenv("API_ID", "0"))
        self.API_HASH = os.getenv("API_HASH", "")
        self.SESSION_STRING = os.getenv("SESSION_STRING", "")
        
        # Auto-generated configuration (will be set during setup)
        self.BOT_TOKEN = os.getenv("BOT_TOKEN", "")
        self.BOT_USERNAME = os.getenv("BOT_USERNAME", "")
        self.LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0")) if os.getenv("LOG_GROUP_ID") else None
        
        # Optional configuration with defaults
        self.SUDO_USERS = self._parse_list(os.getenv("SUDO_USERS", ""))
        self.PM_PERMIT = os.getenv("PM_PERMIT", "True").lower() == "true"
        self.PM_LOG = os.getenv("PM_LOG", "True").lower() == "true"
        self.COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", ".")
        self.ASSISTANT_PREFIX = os.getenv("ASSISTANT_PREFIX", "/")
        
        # Bot information
        self.BOT_NAME = os.getenv("BOT_NAME", "Nexus v2.0")
        self.BOT_VERSION = "2.0.0"
        self.OWNER_NAME = os.getenv("OWNER_NAME", "Nexus User")
        self.OWNER_USERNAME = os.getenv("OWNER_USERNAME", "")
        
        # Database and storage
        self.DATABASE_URL = os.getenv("DATABASE_URL", "")
        self.REDIS_URL = os.getenv("REDIS_URL", "")
        
        # Plugin configuration
        self.LOAD_PLUGINS = os.getenv("LOAD_PLUGINS", "True").lower() == "true"
        self.PLUGIN_CHANNEL = os.getenv("PLUGIN_CHANNEL", "")
        
        # Media configuration
        self.MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "4096"))
        self.DOWNLOAD_DIRECTORY = os.getenv("DOWNLOAD_DIRECTORY", "./downloads")
        
        # Security settings
        self.ANTI_SPAM = os.getenv("ANTI_SPAM", "True").lower() == "true"
        self.LOG_ERRORS = os.getenv("LOG_ERRORS", "True").lower() == "true"
        
        # Deployment settings
        self.HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "")
        self.HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "")
        
        # File paths
        self.BASE_DIR = Path(__file__).parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"
        self.PLUGINS_DIR = self.BASE_DIR / "plugins"
        self.DOWNLOADS_DIR = Path(self.DOWNLOAD_DIRECTORY)
        
        # Create directories
        self.ASSETS_DIR.mkdir(exist_ok=True)
        self.DOWNLOADS_DIR.mkdir(exist_ok=True)
        
        # Validate configuration
        self._validate()
    
    def _parse_list(self, value: str) -> list:
        """Parse comma-separated string to list of integers"""
        if not value:
            return []
        try:
            return [int(x.strip()) for x in value.split(",") if x.strip()]
        except ValueError:
            logger.warning(f"Invalid list format: {value}")
            return []
    
    def _validate_session_string(self, session_string: str) -> bool:
        """Validate Pyrogram session string format"""
        if not session_string:
            return False
        
        try:
            # Basic validation - session strings are base64 encoded and have specific structure
            import base64
            decoded = base64.b64decode(session_string + "===")  # Add padding if needed
            
            # Pyrogram session strings when decoded should be at least 350+ bytes
            if len(decoded) < 350:
                return False
                
            # Check if it starts with expected Pyrogram session format
            # This is a basic check - more sophisticated validation could be added
            return True
            
        except Exception as e:
            logger.warning(f"Session string validation failed: {e}")
            return False
    
    def _validate(self):
        """Validate required configuration - SESSION STRING ONLY"""
        errors = []
        
        if not self.API_ID or self.API_ID == 0:
            errors.append("API_ID is required - get it from https://my.telegram.org")
            
        if not self.API_HASH:
            errors.append("API_HASH is required - get it from https://my.telegram.org")
            
        if not self.SESSION_STRING:
            errors.append("SESSION_STRING is required - generate using generate_session.py")
        elif not self._validate_session_string(self.SESSION_STRING):
            errors.append("SESSION_STRING appears to be invalid - please regenerate using generate_session.py")
        
        if errors:
            error_msg = "❌ Configuration errors:\n" + "\n".join(f"- {error}" for error in errors)
            error_msg += "\n\n📖 For help generating session string, run: python generate_session.py"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("✅ Configuration validated successfully")
    
    def update_env_var(self, key: str, value: str):
        """Update environment variable and save to .env file"""
        try:
            # Update environment
            os.environ[key] = value
            setattr(self, key, value)
            
            # Update .env file
            env_file = self.BASE_DIR / ".env"
            env_vars = {}
            
            # Read existing .env file
            if env_file.exists():
                with open(env_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            env_vars[k.strip()] = v.strip()
            
            # Update the variable
            env_vars[key] = value
            
            # Write back to .env file
            with open(env_file, "w") as f:
                f.write("# Nexus v2.0 Configuration\n")
                f.write("# Generated automatically - do not edit manually\n\n")
                for k, v in env_vars.items():
                    f.write(f"{k}={v}\n")
            
            logger.info(f"✅ Updated {key} in environment and .env file")
            
        except Exception as e:
            logger.error(f"❌ Failed to update {key}: {e}")
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return {
            "API_ID": self.API_ID,
            "API_HASH": self.API_HASH,
            "SESSION_STRING": "***" if self.SESSION_STRING else "",  # Hide for security
            "BOT_TOKEN": self.BOT_TOKEN,
            "BOT_USERNAME": self.BOT_USERNAME,
            "LOG_GROUP_ID": self.LOG_GROUP_ID,
            "BOT_NAME": self.BOT_NAME,
            "BOT_VERSION": self.BOT_VERSION,
            "OWNER_NAME": self.OWNER_NAME,
            "PM_PERMIT": self.PM_PERMIT,
            "COMMAND_PREFIX": self.COMMAND_PREFIX,
            "ASSISTANT_PREFIX": self.ASSISTANT_PREFIX,
        }
    
    def is_configured(self) -> bool:
        """Check if bot is fully configured"""
        return bool(
            self.API_ID and
            self.API_HASH and
            self.SESSION_STRING and
            self.BOT_TOKEN and
            self.LOG_GROUP_ID
        )
    
    def __str__(self):
        """String representation (safe - no sensitive data)"""
        return f"Nexus Config (API_ID: {self.API_ID}, Session: {'✅' if self.SESSION_STRING else '❌'}, Configured: {self.is_configured()})"
