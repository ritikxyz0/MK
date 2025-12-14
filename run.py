#!/usr/bin/env python3
"""
MAIN RUN SCRIPT - Run this to start everything
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check and install required packages"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "pyrogram",
        "sounddevice", 
        "numpy",
        "scipy",
        "pyaudio"
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not found")
            install = input(f"Install {package}? (y/n): ")
            if install.lower() == 'y':
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed")
    
    print("\n✅ All dependencies checked!")

def check_config():
    """Check if config is properly set"""
    print("\n🔧 Checking configuration...")
    
    try:
        from config import API_ID, API_HASH, BOT_TOKEN
        
        if API_ID == 123456:
            print("❌ API_ID is still default (123456)")
            print("Please update config.py with your real API ID")
            return False
        
        if API_HASH == "your_api_hash_here_32_characters":
            print("❌ API_HASH is still default")
            print("Please update config.py with your real API hash")
            return False
        
        if BOT_TOKEN == "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            print("❌ BOT_TOKEN is still default")
            print("Please update config.py with your real bot token")
            return False
        
        print("✅ Configuration is properly set!")
        print(f"📱 API ID: {API_ID}")
        print(f"🔑 API Hash: {API_HASH[:10]}...")
        print(f"🤖 Bot Token: {BOT_TOKEN[:20]}...")
        return True
        
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def print_instructions():
    """Print setup instructions"""
    print("\n" + "="*60)
    print("🎤 VOICE ENHANCER BOT - SETUP INSTRUCTIONS")
    print("="*60)
    
    instructions = """
    📌 REQUIRED SETUP:
    
    1. VIRTUAL AUDIO CABLE (For voice enhancement):
       • Download VB-Cable: https://vb-audio.com/Cable/
       • Install as Administrator
       • Restart computer
       • Set "VB-Cable Input" as default microphone
    
    2. TELEGRAM SETUP:
       • Join any voice chat
       • Click microphone icon
       • Select "VB-Cable Output" as microphone
    
    3. BOT CONTROLS:
       • /start - Show help
       • /startaudio - Begin processing
       • /effects - Change voice effect
       • /gain - Adjust volume
    
    🎯 QUICK START:
    1. Run: python telegram_bot.py
    2. Send /start to your bot
    3. Use /startaudio to begin
    4. Join voice chat and speak!
    
    ⚠️  TROUBLESHOOTING:
    • No sound? Check VB-Cable settings
    • Bot not responding? Check API credentials
    • Echo? Use /gain 2.0
    """
    
    print(instructions)
    print("="*60)

def test_audio():
    """Test audio system"""
    print("\n🎤 Testing audio system...")
    
    try:
        import sounddevice as sd
        
        # List audio devices
        devices = sd.query_devices()
        print(f"\n📱 Found {len(devices)} audio devices:")
        
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"  {i}: {device['name']} (Input)")
        
        # Test microphone
        print("\n🔊 Speak into your microphone...")
        
        import numpy as np
        
        def print_volume(indata, frames, time, status):
            volume_norm = np.linalg.norm(indata) * 10
            print(f"Volume: {'█' * int(volume_norm)}", end='\r')
        
        with sd.InputStream(callback=print_volume):
            sd.sleep(3000)
        
        print("\n✅ Audio test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("🎤 VOICE ENHANCER BOT - LAUNCHER")
    print("="*60)
    
    # Menu
    while True:
        print("\n📋 MAIN MENU:")
        print("1. Install Dependencies")
        print("2. Check Configuration")
        print("3. Test Audio System")
        print("4. Start Telegram Bot")
        print("5. Show Instructions")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            check_dependencies()
            
        elif choice == "2":
            if check_config():
                print("\n✅ Configuration is ready!")
            else:
                print("\n❌ Please update config.py first!")
                print("Open config.py and fill your API credentials")
                input("Press Enter to continue...")
                
        elif choice == "3":
            test_audio()
            
        elif choice == "4":
            print("\n🚀 Starting Telegram Bot...")
            print("Press Ctrl+C to stop\n")
            
            try:
                import telegram_bot
                telegram_bot.main()
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        elif choice == "5":
            print_instructions()
            
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
