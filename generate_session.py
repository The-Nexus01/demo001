"""
Enhanced Session String Generator for Nexus v2.0
Generate Pyrogram session strings securely
Created by: The Nexus Team
GitHub: https://github.com/The-Nexus-Bot/Nexus-Userbot
License: MIT
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from pyrogram import Client
    from pyrogram.errors import ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, SessionPasswordNeeded
except ImportError:
    print("❌ Pyrogram not installed! Install with: pip install pyrogram tgcrypto")
    sys.exit(1)

class SessionGenerator:
    """Enhanced session string generator with validation"""
    
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.phone = None
        self.session_string = None
    
    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "="*60)
        print("🌟 NEXUS v2.0 SESSION STRING GENERATOR 🌟")
        print("="*60)
        print("Generate your Pyrogram session string securely")
        print("This session string will be used instead of phone number")
        print("="*60 + "\n")
    
    def get_credentials(self):
        """Get API credentials from user"""
        print("📋 STEP 1: Get your API credentials")
        print("Visit: https://my.telegram.org/apps")
        print("Create an app and get your API_ID and API_HASH\n")
        
        while True:
            try:
                api_id = input("🔢 Enter your API_ID: ").strip()
                self.api_id = int(api_id)
                if self.api_id <= 0:
                    print("❌ API_ID must be a positive number!")
                    continue
                break
            except ValueError:
                print("❌ Invalid API_ID! Please enter a valid number.")
        
        while True:
            api_hash = input("🔑 Enter your API_HASH: ").strip()
            if len(api_hash) < 10:
                print("❌ API_HASH seems too short! Please check and try again.")
                continue
            self.api_hash = api_hash
            break
        
        print("✅ API credentials received\n")
    
    def get_phone_number(self):
        """Get phone number from user"""
        print("📱 STEP 2: Enter your phone number")
        print("Include country code (e.g., +1234567890)")
        print("This is only used once to generate the session string\n")
        
        while True:
            phone = input("📞 Enter your phone number: ").strip()
            if not phone.startswith('+'):
                phone = '+' + phone
            
            if len(phone) < 8:
                print("❌ Phone number seems too short! Please include country code.")
                continue
            
            self.phone = phone
            break
        
        print("✅ Phone number received\n")
    
    async def generate_session(self):
        """Generate session string"""
        print("🔄 STEP 3: Generating session string...")
        print("You will receive a login code via Telegram\n")
        
        # Create temporary client
        temp_client = Client(
            name="temp_session",
            api_id=self.api_id,
            api_hash=self.api_hash,
            phone_number=self.phone,
            in_memory=True  # Don't save session file
        )
        
        try:
            # Start client and handle authentication
            await temp_client.start()
            
            # Get session string
            self.session_string = await temp_client.export_session_string()
            
            # Get user info
            me = await temp_client.get_me()
            
            # Stop client
            await temp_client.stop()
            
            print("✅ Session string generated successfully!\n")
            print("👤 Account Information:")
            print(f"   Name: {me.first_name} {me.last_name or ''}")
            print(f"   Username: @{me.username or 'N/A'}")
            print(f"   ID: {me.id}")
            print(f"   Phone: {me.phone_number}")
            
            return True
            
        except ApiIdInvalid:
            print("❌ Invalid API_ID or API_HASH! Please check your credentials.")
            return False
        except PhoneNumberInvalid:
            print("❌ Invalid phone number! Please check and try again.")
            return False
        except Exception as e:
            print(f"❌ Error during authentication: {e}")
            return False
    
    def save_session(self):
        """Save session string to file and display"""
        print("\n" + "="*60)
        print("🎉 SESSION STRING GENERATED SUCCESSFULLY!")
        print("="*60)
        print("📝 Your session string:")
        print("\n" + "="*60)
        print(self.session_string)
        print("="*60 + "\n")
        
        # Save to file
        session_file = Path("session_string.txt")
        try:
            with open(session_file, "w") as f:
                f.write(self.session_string)
            print(f"💾 Session string saved to: {session_file.absolute()}")
        except Exception as e:
            print(f"⚠️ Could not save to file: {e}")
        
        # Create .env file
        env_file = Path(".env")
        try:
            env_content = f"""# Nexus v2.0 Configuration
# Add your API credentials and session string below

API_ID={self.api_id}
API_HASH={self.api_hash}
SESSION_STRING={self.session_string}

# Optional: Bot configuration (will be auto-generated if not provided)
# BOT_TOKEN=
# LOG_GROUP_ID=
# OWNER_NAME=Your Name
"""
            with open(env_file, "w") as f:
                f.write(env_content)
            print(f"📄 Configuration template saved to: {env_file.absolute()}")
        except Exception as e:
            print(f"⚠️ Could not create .env file: {e}")
        
        print("\n🔒 SECURITY NOTES:")
        print("• Keep your session string private and secure")
        print("• Never share it with anyone")
        print("• If compromised, regenerate immediately")
        print("• This session string replaces phone number authentication")
        
        print("\n📖 NEXT STEPS:")
        print("1. Copy the session string to your deployment environment")
        print("2. Set SESSION_STRING environment variable")
        print("3. Deploy your Nexus userbot")
        print("4. Enjoy automated Telegram features!")
        
        print("\n✨ Your Nexus userbot is ready to deploy!")

async def main():
    """Main function"""
    generator = SessionGenerator()
    
    try:
        generator.print_banner()
        generator.get_credentials()
        generator.get_phone_number()
        
        success = await generator.generate_session()
        if success:
            generator.save_session()
        else:
            print("\n❌ Session generation failed. Please try again.")
            return
        
    except KeyboardInterrupt:
        print("\n\n👋 Session generation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def validate_existing_session():
    """Validate an existing session string"""
    print("\n🔍 SESSION STRING VALIDATOR")
    print("="*40)
    
    session = input("Enter your session string to validate: ").strip()
    
    if not session:
        print("❌ Empty session string!")
        return
    
    try:
        import base64
        decoded = base64.b64decode(session + "===")
        
        if len(decoded) < 350:
            print("❌ Session string appears to be invalid (too short)")
        else:
            print("✅ Session string format looks valid")
            print(f"📏 Length: {len(session)} characters")
            print(f"📦 Decoded size: {len(decoded)} bytes")
    
    except Exception as e:
        print(f"❌ Invalid session string format: {e}")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Generate new session string")
    print("2. Validate existing session string")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(main())
    elif choice == "2":
        validate_existing_session()
    else:
        print("❌ Invalid choice!")
