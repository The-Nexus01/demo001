# 🚀 Quick Deploy Guide - Nexus v2.0

## Step 1: Get Your Credentials

### Get API Credentials (2 minutes)
1. Go to https://my.telegram.org
2. Login with your phone number
3. Click "API development tools"
4. Create new app (any name/description)
5. Copy your `API_ID` and `API_HASH`

### Generate Session String (3 minutes)
1. Download this repository or use online tools
2. Run: `python generate_session.py`
3. Enter your API_ID, API_HASH, and phone number
4. Enter the verification code sent to your phone
5. Copy the session string

## Step 2: Deploy (1 click)

### Heroku (Easiest)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/The-Nexus-Bot/Nexus-Userbot)

1. Click the button above
2. Fill in: API_ID, API_HASH, SESSION_STRING
3. Click "Deploy app"
4. Done! ✅

### Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/The-Nexus-Bot/Nexus-Userbot)

1. Click the button above
2. Connect GitHub and fork repository
3. Set environment variables
4. Deploy ✅

### Railway  
[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/nexus-userbot)

1. Click the button above
2. Connect GitHub
3. Set environment variables
4. Deploy ✅

## Step 3: Verify (30 seconds)

1. Check deployment logs
2. Look for "✅ Nexus v2.0 logging initialized"
3. No configuration errors = Success! 🎉

## That's it!

Your userbot is now running 24/7 in the cloud with:
- ✅ Session string authentication (no phone needed)
- ✅ Auto-setup for assistant bot and log group
- ✅ All plugins loaded and ready
- ✅ PM protection and anti-spam enabled

## Need Help?

- Check logs for any errors
- Verify environment variables are set correctly
- Make sure session string is valid
- See DEPLOYMENT.md for detailed troubleshooting

**Total time: ~6 minutes** ⚡