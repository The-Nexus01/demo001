# 🚀 Nexus v2.0 - Advanced Telegram Userbot

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0+-green.svg)](https://pyrogram.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Ready-brightgreen.svg)](#deployment)

> **Session String Authentication Only** - No phone numbers required for deployment!

Nexus v2.0 is a sophisticated Telegram userbot built with Python and Pyrogram. Features hybrid architecture with both userbot and assistant bot capabilities, automatic setup, and a modular plugin system designed for automation and enhanced Telegram functionality.

## ✨ Key Features

- **🔐 Session String Authentication** - No phone number verification needed
- **🤖 Hybrid Bot System** - Userbot + Assistant bot in one
- **☁️ Cloud Ready** - Deploy anywhere without interactive setup
- **🔧 Auto Setup** - Automatic bot creation and configuration
- **📱 Plugin System** - Modular and extensible
- **🛡️ Security First** - Built-in validation and protection
- **📊 Advanced Logging** - Comprehensive error tracking

## 🚦 Quick Start

### 1. Get API Credentials
1. Visit [my.telegram.org](https://my.telegram.org)
2. Login with your Telegram account
3. Create a new application
4. Note down your `API_ID` and `API_HASH`

### 2. Generate Session String
```bash
python generate_session.py
```
Follow the interactive prompts to create your session string.

### 3. Configure Environment
Set these environment variables:
```bash
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_STRING=your_session_string
```

### 4. Run the Bot
```bash
python main.py
```

## 📋 Required Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `API_ID` | Telegram API ID from my.telegram.org | ✅ Yes |
| `API_HASH` | Telegram API Hash from my.telegram.org | ✅ Yes |
| `SESSION_STRING` | Generated session string | ✅ Yes |
| `BOT_TOKEN` | Assistant bot token (auto-generated) | ❌ Optional |
| `LOG_GROUP_ID` | Log group ID (auto-created) | ❌ Optional |

## 🚀 One-Click Deployment

### Deploy Instantly:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/The-Nexus-Bot/Nexus-Userbot)

[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/nexus-userbot)

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/The-Nexus-Bot/Nexus-Userbot)

## 🌐 Deployment Options

### 🐳 Docker Deployment (Recommended)

**Quick Start with Docker:**
```bash
# Clone repository
git clone https://github.com/The-Nexus-Bot/Nexus-Userbot.git
cd Nexus-Userbot

# Create environment file
cp .env.example .env
# Edit .env with your credentials

# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f nexus-userbot
```

**Manual Docker Build:**
```bash
# Build image
docker build -t nexus-userbot .

# Run container
docker run -d \
  --name nexus-userbot \
  --restart unless-stopped \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  -e SESSION_STRING=your_session_string \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/downloads:/app/downloads \
  nexus-userbot
```

### ☁️ Cloud Platform Deployment

**Deploy on Render:**
1. Fork this repository
2. Connect to [Render](https://render.com)
3. Create new Web Service from your fork
4. Set environment variables in dashboard
5. Deploy using the provided `render.yaml`

**Deploy on Koyeb:**
1. Fork this repository to your GitHub account
2. Connect to [Koyeb](https://koyeb.com)
3. Import from GitHub and select your fork
4. Set environment variables (API_ID, API_HASH, SESSION_STRING)
5. Deploy automatically - dependencies will be detected from requirements.txt

**Deploy on Heroku:**
1. Use the `app.json` for app store deployment
2. Click "Deploy to Heroku"
3. Configure environment variables

## 🔧 Advanced Configuration

<details>
<summary>Optional Environment Variables</summary>

| Variable | Default | Description |
|----------|---------|-------------|
| `OWNER_NAME` | "Nexus User" | Your display name |
| `OWNER_USERNAME` | - | Your Telegram username |
| `BOT_NAME` | "Nexus v2.0" | Assistant bot name |
| `COMMAND_PREFIX` | "." | Userbot command prefix |
| `ASSISTANT_PREFIX` | "/" | Assistant bot prefix |
| `PM_PERMIT` | True | Private message protection |
| `PM_LOG` | True | Log private messages |
| `ANTI_SPAM` | True | Anti-spam protection |
| `LOG_ERRORS` | True | Error logging |
| `LOAD_PLUGINS` | True | Enable plugin system |

</details>

## 📚 Session String Guide

### What is a Session String?
A session string is an encrypted authentication token that contains your Telegram login session. It allows the bot to connect to Telegram without requiring your phone number or password.

### Benefits of Session String Authentication
- **No Phone Verification** - Deploy without interactive authentication
- **Cloud Friendly** - Perfect for automated deployments
- **Secure** - Encrypted authentication data
- **Portable** - Use across multiple deployments

### Generating Session String
```bash
# Interactive session generator
python generate_session.py

# Validate existing session
python -c "from utils.session_validator import validate_session_string; print(validate_session_string('your_session_string'))"
```

## 🔍 Session String Validation

The bot includes advanced session string validation:

```python
from utils.session_validator import SessionValidator

# Validate format
result = SessionValidator.validate_format(session_string)
print(f"Valid: {result['valid']}")
print(f"Security Score: {result['security_score']}/10")

# Get detailed analysis
analysis = SessionValidator.analyze_session(session_string)
```

## 🏗️ Project Structure

```
nexus-userbot/
├── bot/                    # Core bot module
│   ├── client.py          # Enhanced Pyrogram client
│   ├── logger.py          # Logging configuration
│   └── setup.py           # Auto-setup manager
├── utils/                  # Utility functions
│   └── session_validator.py # Session validation
├── config.py              # Configuration management
├── main.py                # Application entry point
├── generate_session.py    # Session string generator
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker Compose setup
├── .env.example           # Environment variables template
├── render.yaml           # Render deployment config
├── koyeb.yaml            # Koyeb deployment config
├── app.json              # Heroku app store config
├── requirements.txt      # Python dependencies
├── requirements-build.txt # Build-specific dependencies  
├── pyproject.toml        # Modern Python package configuration
├── startup.py            # Deployment startup script
├── DEPLOYMENT.md         # Comprehensive deployment guide
└── QUICK_DEPLOY.md       # Quick deployment instructions
```

## 🚀 Development

### Local Development
```bash
# Clone repository
git clone https://github.com/your-username/nexus-userbot.git
cd nexus-userbot

# Install dependencies
pip install -r dependencies.txt

# Generate session string
python generate_session.py

# Run bot
python main.py
```

### Adding Plugins
1. Create plugin file in `plugins/` directory
2. Use Pyrogram decorators for handlers
3. Bot will automatically load on restart

## 🛡️ Security Features

- **Session String Validation** - Format and integrity checks
- **Environment Variable Protection** - No hardcoded credentials
- **Auto-generated Tokens** - Secure bot token creation
- **PM Protection** - Private message filtering
- **Anti-spam System** - Built-in spam detection
- **Secure Logging** - Error tracking without sensitive data

## ❓ Troubleshooting

### Common Issues

**Configuration Error: Missing API credentials**
```
Solution: Get API_ID and API_HASH from https://my.telegram.org
```

**Session String Invalid**
```bash
# Validate your session string
python generate_session.py
# Choose option 2 to validate existing session
```

**Bot Not Starting**
```
Check logs in logs/nexus.log for detailed error information
```

### Getting Help

1. Check the [Session Guide](SESSION_GUIDE.md)
2. Review [Environment Variables](ENV_VARIABLES.txt)
3. Validate your configuration:
   ```bash
   python -c "from config import Config; config = Config(); print('✅ Configuration valid' if config.is_configured() else '❌ Configuration invalid')"
   ```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This userbot is for educational and automation purposes only. Users are responsible for complying with Telegram's Terms of Service and local laws. The developers are not responsible for any misuse of this software.

## 🌟 Support

- **GitHub Issues**: [Report bugs](https://github.com/your-username/nexus-userbot/issues)
- **Documentation**: [Full docs](https://github.com/your-username/nexus-userbot/wiki)
- **Telegram**: [@NexusSupport](https://t.me/NexusSupport)

---

<div align="center">

**Made with ❤️ by The Nexus Team**

[⭐ Star this repo](https://github.com/your-username/nexus-userbot) • [🐛 Report bug](https://github.com/your-username/nexus-userbot/issues) • [💡 Request feature](https://github.com/your-username/nexus-userbot/issues)

</div>