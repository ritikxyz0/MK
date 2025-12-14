"""
CONFIGURATION FILE
Fill your Telegram API credentials here
"""

# Telegram API Credentials (Get from https://my.telegram.org)
API_ID = 39496551  # YOUR_API_ID_HERE (number only)
API_HASH = "36495414098630fed4555734bcc9748b"  # YOUR_API_HASH_HERE

# Bot Token (Get from @BotFather on Telegram)
BOT_TOKEN = "8517043316:AAH31rVstixRMVolYwkShcqxiGCxi2kLD8s"  # YOUR_BOT_TOKEN_HERE

# Audio Settings
SAMPLE_RATE = 48000  # Audio sample rate
CHUNK_SIZE = 1024    # Audio chunk size
CHANNELS = 1         # Mono audio

# Voice Effects Configuration
EFFECTS_CONFIG = {
    "normal": {"name": "Normal Voice", "gain": 1.0, "bass": 0.0, "treble": 0.0},
    "hige": {"name": "High Gain", "gain": 2.5, "bass": 0.7, "treble": 0.3},
    "ultra": {"name": "Ultra High", "gain": 3.5, "bass": 0.9, "treble": 0.5},
    "bass": {"name": "Bass Boost", "gain": 2.0, "bass": 1.2, "treble": 0.1},
    "clear": {"name": "Clear Voice", "gain": 2.2, "bass": 0.3, "treble": 0.8},
    "robot": {"name": "Robot Voice", "gain": 2.5, "bass": 0.5, "treble": 0.9}
}

# Virtual Audio Cable Settings (Windows)
VB_CABLE_INPUT = "CABLE Input (VB-Audio Virtual Cable)"  # Virtual cable input name
VB_CABLE_OUTPUT = "CABLE Output (VB-Audio Virtual Cable)"  # Virtual cable output name
