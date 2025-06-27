# 🚀 Nexus v2.0 - Complete Deployment Guide

## Prerequisites

Before deploying, you need:

1. **Telegram API Credentials**
   - Go to https://my.telegram.org
   - Login with your Telegram account
   - Create a new app (any name works)
   - Copy your `API_ID` and `API_HASH`

2. **Session String**
   - Clone this repository locally
   - Run: `python generate_session.py`
   - Enter your API credentials and phone number
   - Copy the generated session string

## 🎯 One-Click Deployment

### Heroku (Recommended for Beginners)

1. Click: [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/The-Nexus-Bot/Nexus-Userbot)

2. Fill in the required environment variables:
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API Hash  
   - `SESSION_STRING`: Generated session string

3. Click "Deploy app"

4. Wait for deployment to complete

5. Go to "More" → "View logs" to check if bot started successfully

### Render

1. Click: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/The-Nexus-Bot/Nexus-Userbot)

2. Connect your GitHub account

3. Fork the repository to your account

4. Set environment variables in Render dashboard:
   - `API_ID`: Your API ID
   - `API_HASH`: Your API Hash
   - `SESSION_STRING`: Your session string

5. Deploy the service

### Railway

1. Click: [![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/nexus-userbot)

2. Connect GitHub and fork the repository

3. Set environment variables:
   - `API_ID`
   - `API_HASH` 
   - `SESSION_STRING`

4. Deploy

## 🐳 Docker Deployment

### Quick Docker Setup

```bash
# Clone repository
git clone https://github.com/The-Nexus-Bot/Nexus-Userbot.git
cd Nexus-Userbot

# Create environment file
cp .env.example .env

# Edit .env with your credentials
nano .env

# Run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f nexus-userbot
```

### Manual Docker Build

```bash
# Build image
docker build -t nexus-userbot .

# Run container
docker run -d \\
  --name nexus-userbot \\
  --restart unless-stopped \\
  -e API_ID=your_api_id \\
  -e API_HASH=your_api_hash \\
  -e SESSION_STRING=your_session_string \\
  -v $(pwd)/logs:/app/logs \\
  nexus-userbot
```

## 🔧 Manual Platform Deployment

### Koyeb

1. Fork this repository to your GitHub

2. Go to https://koyeb.com and create account

3. Create new app from GitHub

4. Select your forked repository

5. Set environment variables:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   SESSION_STRING=your_session_string
   ```

6. Deploy

### VPS/Server Deployment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-pip git -y

# Clone repository
git clone https://github.com/The-Nexus-Bot/Nexus-Userbot.git
cd Nexus-Userbot

# Install dependencies
pip3.11 install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit environment variables
nano .env

# Run bot
python3.11 main.py

# Or run in background with screen
screen -S nexus
python3.11 main.py
# Press Ctrl+A then D to detach
```

## 📋 Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `API_ID` | Telegram API ID | `12345678` |
| `API_HASH` | Telegram API Hash | `abcd1234...` |
| `SESSION_STRING` | Pyrogram session string | `1BVtsOK4...` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BOT_TOKEN` | Auto-generated | Assistant bot token |
| `LOG_GROUP_ID` | Auto-created | Log group chat ID |
| `OWNER_NAME` | "Nexus User" | Your display name |
| `OWNER_USERNAME` | Empty | Your Telegram username |
| `BOT_NAME` | "Nexus v2.0" | Bot display name |
| `COMMAND_PREFIX` | "." | Userbot command prefix |
| `ASSISTANT_PREFIX` | "/" | Assistant bot prefix |
| `PM_PERMIT` | True | PM protection |
| `PM_LOG` | True | Log private messages |
| `ANTI_SPAM` | True | Anti-spam protection |
| `LOG_ERRORS` | True | Error logging |
| `LOAD_PLUGINS` | True | Auto-load plugins |

## 🔍 Troubleshooting

### Common Issues

**1. "Module not found" error**
- Make sure `requirements.txt` is in the root directory
- Verify all dependencies are installed
- Check Python version (3.11+ required)

**2. "Configuration errors" on startup**
- Verify API_ID and API_HASH are correct
- Check session string is valid
- Ensure environment variables are set properly

**3. Session string issues**
- Generate new session string locally
- Make sure phone number format is correct
- Try different session generation methods

**4. Bot not responding**
- Check if bot started successfully in logs
- Verify session string hasn't expired
- Ensure Telegram account isn't restricted

### Getting Help

1. Check deployment logs first
2. Verify all environment variables are set
3. Test session string locally before deploying
4. Create GitHub issue if problems persist

## 🔐 Security Best Practices

1. **Never share your session string**
2. **Keep API credentials private**
3. **Use environment variables, never hardcode**
4. **Regularly rotate session strings**
5. **Monitor deployment logs for errors**

## ✅ Verification Steps

After deployment:

1. Check logs show "Nexus v2.0 logging initialized"
2. Verify no configuration errors in logs
3. Test bot responds to commands
4. Check assistant bot is created (if configured)
5. Verify log group is working (if configured)

## 🎉 Success!

Your Nexus userbot should now be running! The bot will:
- Auto-create assistant bot if needed
- Set up log group automatically
- Load all plugins
- Start responding to commands

Happy automating! 🚀