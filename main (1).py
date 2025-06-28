"""
Nexus v2.0 - Advanced Telegram Userbot
Main entry point with session string authentication only
Created by: The Nexus Team
GitHub: https://github.com/The-Nexus-Bot/Nexus-Userbot
License: MIT
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from aiohttp import web
from bot.client import NexusClient
from bot.logger import setup_logging
from config import Config

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

async def health_check(request):
    """Health check endpoint for deployment platforms."""
    return web.Response(text="Nexus v2.0 is running!", status=200)

async def create_health_server():
    """Create a simple health check server for deployment platforms."""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)

    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    return runner, port

class NexusBot:
    """Main Nexus Bot class with session string authentication only"""

    def __init__(self):
        self.config = Config()
        self.userbot = None
        self.assistant = None
        self.setup_manager = None

    async def initialize(self):
        """Initialize the bot with automatic setup"""
        try:
            logger.info("🌟 Starting Nexus v2.0 initialization...")

            # Validate session string before proceeding
            if not self.config.SESSION_STRING:
                logger.error("❌ SESSION_STRING is required! Please generate one using generate_session.py")
                return False

            # Initialize auto-setup manager
            self.setup_manager = AutoSetup(self.config)

            # Run automatic setup if needed
            setup_success = await self.setup_manager.run_setup()
            if not setup_success:
                logger.error("❌ Auto-setup failed. Please check your configuration.")
                return False

            # Initialize userbot client with session string only
            logger.info("🚀 Initializing userbot client with session string...")
            self.userbot = NexusClient(
                name="nexus_userbot",
                api_id=self.config.API_ID,
                api_hash=self.config.API_HASH,
                session_string=self.config.SESSION_STRING,
                is_assistant=False,
                config=self.config
            )

            # Initialize assistant bot if token is available
            if self.config.BOT_TOKEN:
                logger.info("🤖 Initializing assistant bot...")
                self.assistant = NexusClient(
                    name="nexus_assistant",
                    api_id=self.config.API_ID,
                    api_hash=self.config.API_HASH,
                    bot_token=self.config.BOT_TOKEN,
                    is_assistant=True,
                    config=self.config
                )

            return True

        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            return False

    async def start(self):
        """Start both userbot and assistant bot"""
        try:
            # Start health check server for deployment platforms
            runner, port = await create_health_server()
            logger.info(f"🌐 Health check server started on port {port}")

            # Start userbot
            logger.info("🔄 Starting userbot...")
            await self.userbot.start()
            logger.info("✅ Userbot started successfully")

            # Start assistant bot if available
            if self.assistant:
                logger.info("🔄 Starting assistant bot...")
                await self.assistant.start()
                logger.info("✅ Assistant bot started successfully")

            # Keep the bot running
            logger.info("🎉 Nexus v2.0 is now running!")
            await asyncio.Event().wait()

        except KeyboardInterrupt:
            logger.info("🛑 Received stop signal")
        except Exception as e:
            logger.error(f"❌ Runtime error: {e}")
        finally:
            await self.stop(runner)

    async def stop(self, runner):
        """Stop all clients gracefully"""
        try:
            logger.info("🔄 Stopping Nexus...")

            if self.userbot and self.userbot.is_connected:
                await self.userbot.stop()
                logger.info("✅ Userbot stopped")

            if self.assistant and self.assistant.is_connected:
                await self.assistant.stop()
                logger.info("✅ Assistant bot stopped")

            logger.info("👋 Nexus v2.0 stopped gracefully")

        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")
        finally:
            if 'runner' in locals():
                await runner.cleanup()

async def main():
    """Main function"""
    bot = NexusBot()

    # Initialize the bot
    if not await bot.initialize():
        sys.exit(1)

    # Start the bot
    await bot.start()

if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)