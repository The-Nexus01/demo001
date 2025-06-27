# Nexus v2.0 - Advanced Telegram Userbot

## Overview

Nexus v2.0 is a sophisticated Telegram userbot built with Python and Pyrogram. It features a hybrid architecture with both userbot and assistant bot capabilities, session string authentication (no phone numbers required), automatic setup, and a modular plugin system. The application is designed for automation, messaging management, and enhanced Telegram functionality.

## System Architecture

### Hybrid Bot Architecture
The system operates with two distinct client types:
- **Userbot Client**: Primary user automation interface using session string authentication
- **Assistant Bot Client**: Secondary bot for public commands and logging
- **Auto-Setup Manager**: Handles automatic configuration and bot creation during first run

### Authentication Strategy (Updated)
- **Session String Only**: Phone number requirements completely removed ✅
- **Security-First**: Uses Pyrogram session strings for persistent authentication
- **Deployment-Ready**: Designed for cloud platforms without interactive authentication
- **No Phone Numbers**: Authentication is 100% session string based

## Key Components

### Core Application (`main.py`)
- Main entry point with initialization logic
- Session string validation before startup
- Automatic setup orchestration
- Error handling and recovery mechanisms

### Configuration Management (`config.py`)
- Environment-based configuration system
- Session string validation
- Auto-generated settings for bot tokens and groups
- Feature toggles for PM protection, logging, and plugins

### Session Management
- **Session Generator** (`generate_session.py`): Interactive tool for creating session strings
- **Session Validator** (`utils/session_validator.py`): Format validation and security checks
- **No Phone Numbers**: Complete elimination of phone-based authentication

### Client Architecture (`bot/client.py`)
- Enhanced Pyrogram client wrapper
- Plugin system integration
- Command handling for both userbot and assistant
- Automatic reconnection and error recovery

### Auto-Setup System (`bot/setup.py`)
- Automatic bot creation via BotFather
- Log group creation and configuration
- Environment variable updates
- First-run initialization

## Data Flow

1. **Initialization**: Validate session string and API credentials
2. **Auto-Setup**: Create assistant bot and log group if needed
3. **Client Connection**: Establish userbot and assistant connections
4. **Plugin Loading**: Dynamically load enabled plugins
5. **Command Processing**: Handle commands from both userbot and assistant
6. **Logging**: Route errors and activities to designated log group

## External Dependencies

### Core Dependencies
- **Pyrogram**: Telegram MTProto API framework
- **TGCrypto**: Cryptographic acceleration for Pyrogram
- **tlgbotfwk**: Additional bot framework utilities

### Telegram API Integration
- **API Credentials**: API_ID and API_HASH from my.telegram.org
- **BotFather Integration**: Automatic bot creation and token management
- **Group Management**: Automatic log group creation and administration

### Optional Services
- **Database**: Configurable database URL for persistent storage
- **Redis**: Optional Redis integration for caching
- **Plugin Channels**: External plugin update channels

## Deployment Strategy

### Cloud Platform Support
- **Multi-Platform**: Supports Render, Koyeb, Heroku, and Railway
- **Environment Variables**: Comprehensive configuration via environment
- **No Interactive Auth**: Fully automated deployment without user interaction

### Configuration Files
- **Render**: `render.yaml` with service configuration
- **Koyeb**: `koyeb.yaml` with deployment settings
- **App Store**: `app.json` for platform marketplace deployment
- **Dependencies**: `pyproject.toml` for Python package management

### Security Considerations
- Session strings stored as environment variables
- No hardcoded credentials in source code
- Optional PM protection and anti-spam features
- Secure log group creation and management

## Changelog

```
Changelog:
- June 27, 2025: Removed phone number requirements completely
- June 27, 2025: Implemented session string only authentication  
- June 27, 2025: Updated all deployment configurations
- June 27, 2025: Fixed render.yaml and configuration files
- June 27, 2025: Enhanced session validation and generation
- June 27, 2025: Added one-click deploy buttons for Heroku, Render, Railway
- June 27, 2025: Created comprehensive deployment guides (DEPLOYMENT.md, QUICK_DEPLOY.md)
- June 27, 2025: Fixed deployment build issues by creating requirements.txt
- June 27, 2025: Added Docker support with Dockerfile and docker-compose.yml
- June 27, 2025: Created comprehensive README.md with deployment guides
- June 27, 2025: Removed unnecessary files and created .gitignore
- June 27, 2025: Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```