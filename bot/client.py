"""
Nexus Client - Enhanced Pyrogram client with session string authentication only
Created by: The Nexus Team
GitHub: https://github.com/The-Nexus-Bot/Nexus-Userbot
License: MIT
"""

import asyncio
import logging
import os
import importlib
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

from pyrogram.client import Client
from pyrogram import filters
from pyrogram.errors import FloodWait, AuthKeyUnregistered
from pyrogram.types import Message

logger = logging.getLogger(__name__)

class NexusClient(Client):
    """Enhanced Pyrogram client with session string authentication only"""
    
    def __init__(
        self,
        name: str,
        config,
        is_assistant: bool = False,
        **kwargs
    ):
        # Initialize client configuration
        self.config = config
        self.is_assistant = is_assistant
        self.is_userbot = not is_assistant
        self.plugins = {}
        self.commands = {}
        self.loaded_plugins = set()
        
        # Client session configuration
        session_name = f"{name}_session"
        workdir = config.BASE_DIR / "sessions"
        workdir.mkdir(exist_ok=True)
        
        # Prepare client arguments
        client_args = {
            "name": session_name,
            "api_id": config.API_ID,
            "api_hash": config.API_HASH,
            "workdir": str(workdir),
            "plugins": None,  # We'll handle plugins manually
            **kwargs
        }
        
        # Add authentication method
        if is_assistant and config.BOT_TOKEN:
            # Assistant bot uses bot token
            client_args["bot_token"] = config.BOT_TOKEN
        elif not is_assistant:
            # Userbot MUST use session string - no phone number fallback
            if not config.SESSION_STRING:
                raise ValueError("SESSION_STRING is required for userbot authentication! Generate one using generate_session.py")
            client_args["session_string"] = config.SESSION_STRING
        else:
            raise ValueError("Invalid client configuration - missing authentication method")
        
        # Initialize Pyrogram client
        super().__init__(**client_args)
        
        # Set client attributes
        self.start_time = None
        self.command_prefix = config.COMMAND_PREFIX if not is_assistant else config.ASSISTANT_PREFIX
        
        logger.info(f"✅ Initialized {'Assistant Bot' if is_assistant else 'Userbot'} client with {'bot token' if is_assistant else 'session string'}")
    
    async def start(self):
        """Start the client and load plugins"""
        try:
            # Validate session string for userbot
            if self.is_userbot and not self.config.SESSION_STRING:
                raise ValueError("SESSION_STRING is required! Please generate one using generate_session.py")
            
            # Start Pyrogram client
            await super().start()
            
            # Get bot info
            me = await self.get_me()
            self.me = me
            
            client_type = "Assistant Bot" if self.is_assistant else "Userbot"
            logger.info(f"✅ {client_type} started: @{me.username or 'N/A'} ({me.id})")
            
            # Load plugins
            await self.load_plugins()
            
            # Set start time
            import time
            self.start_time = time.time()
            
            # Send startup message to log group
            if self.config.LOG_GROUP_ID:
                startup_msg = self._get_startup_message()
                try:
                    await self.send_message(self.config.LOG_GROUP_ID, startup_msg)
                except Exception as e:
                    logger.warning(f"Could not send startup message: {e}")
            
        except AuthKeyUnregistered:
            logger.error("❌ Session string is invalid or expired! Please regenerate using generate_session.py")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to start client: {e}")
            raise
    
    async def load_plugins(self):
        """Load all plugins from the plugins directory"""
        try:
            plugins_dir = self.config.PLUGINS_DIR
            if not plugins_dir.exists():
                logger.warning(f"Plugins directory not found: {plugins_dir}")
                return
            
            # Get all Python files in plugins directory
            plugin_files = list(plugins_dir.glob("*.py"))
            plugin_files = [f for f in plugin_files if not f.name.startswith("__")]
            
            logger.info(f"🔌 Loading {len(plugin_files)} plugins...")
            
            for plugin_file in plugin_files:
                await self.load_plugin(plugin_file.stem)
            
            logger.info(f"✅ Loaded {len(self.loaded_plugins)} plugins successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load plugins: {e}")
    
    async def load_plugin(self, plugin_name: str):
        """Load a specific plugin"""
        try:
            # Import the plugin module
            module_name = f"plugins.{plugin_name}"
            
            # Remove from sys.modules if already loaded (for hot reload)
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            # Import the module
            module = importlib.import_module(module_name)
            
            # Check if plugin has setup function
            if hasattr(module, "setup"):
                await module.setup(self)
            
            # Register plugin
            self.plugins[plugin_name] = module
            self.loaded_plugins.add(plugin_name)
            
            logger.info(f"✅ Loaded plugin: {plugin_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load plugin {plugin_name}: {e}")
    
    async def unload_plugin(self, plugin_name: str):
        """Unload a specific plugin"""
        try:
            if plugin_name in self.plugins:
                module = self.plugins[plugin_name]
                
                # Call cleanup function if available
                if hasattr(module, "cleanup"):
                    await module.cleanup(self)
                
                # Remove from loaded plugins
                del self.plugins[plugin_name]
                self.loaded_plugins.discard(plugin_name)
                
                # Remove from sys.modules
                module_name = f"plugins.{plugin_name}"
                if module_name in sys.modules:
                    del sys.modules[module_name]
                
                logger.info(f"✅ Unloaded plugin: {plugin_name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to unload plugin {plugin_name}: {e}")
            return False
    
    async def reload_plugin(self, plugin_name: str):
        """Reload a specific plugin"""
        await self.unload_plugin(plugin_name)
        await self.load_plugin(plugin_name)
    
    def add_command(self, command_name: str, handler, description: str = ""):
        """Add a command handler"""
        self.commands[command_name] = {
            "handler": handler,
            "description": description,
            "client_type": "assistant" if self.is_assistant else "userbot"
        }
    
    def _get_startup_message(self):
        """Get startup message for log group"""
        client_type = "🤖 Assistant Bot" if self.is_assistant else "👤 Userbot"
        auth_method = "Bot Token" if self.is_assistant else "Session String"
        
        return (
            f"🌟 **Nexus v{self.config.BOT_VERSION} Started**\n\n"
            f"{client_type} is now online!\n"
            f"**User:** @{self.me.username or 'N/A'} ({self.me.id})\n"
            f"**Auth:** {auth_method}\n"
            f"**Plugins:** {len(self.loaded_plugins)} loaded\n"
            f"**Commands:** {len(self.commands)} available\n"
            f"**Prefix:** `{self.command_prefix}`"
        )
    
    async def send_log(self, message: str, chat_id: Optional[int] = None):
        """Send message to log group"""
        try:
            log_chat = chat_id or self.config.LOG_GROUP_ID
            if log_chat:
                await self.send_message(log_chat, message)
        except Exception as e:
            logger.warning(f"Failed to send log message: {e}")
    
    async def handle_error(self, error: Exception, context: str = ""):
        """Handle and log errors"""
        error_msg = f"❌ **Error in {context}**\n\n`{str(error)}`"
        logger.error(f"Error in {context}: {error}")
        
        if self.config.LOG_ERRORS:
            await self.send_log(error_msg)
    
    def get_uptime(self) -> str:
        """Get bot uptime"""
        if not self.start_time:
            return "Unknown"
        
        import time
        uptime_seconds = int(time.time() - self.start_time)
        
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def is_sudo(self, user_id: int) -> bool:
        """Check if user is sudo user"""
        return user_id in self.config.SUDO_USERS or user_id == self.me.id
    
    async def restart(self):
        """Restart the client"""
        logger.info("🔄 Restarting client...")
        await self.stop()
        await asyncio.sleep(2)
        await self.start()
