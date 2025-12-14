#!/usr/bin/env python3
"""
AUDIO SETUP HELPER - For Virtual Audio Cable setup
"""

import platform
import sys

def print_windows_setup():
    """Print Windows VB-Cable setup instructions"""
    print("""
    =============================================
    🎤 WINDOWS AUDIO SETUP (VB-CABLE)
    =============================================
    
    STEP 1: INSTALL VB-CABLE
    -------------------------
    1. Download from: https://vb-audio.com/Cable/
    2. Run VBCABLE_Setup.exe as Administrator
    3. Click "Install Driver"
    4. Restart your computer
    
    STEP 2: CONFIGURE AUDIO SETTINGS
    ---------------------------------
    1. Right-click speaker icon in taskbar
    2. Select "Sound settings"
    3. Under "Input", set "CABLE Input" as default
    4. Under "Output", set "CABLE Output" as default
    
    STEP 3: TELEGRAM SETUP
    -----------------------
    1. Join Telegram voice chat
    2. Click microphone icon
    3. Select "CABLE Output" as microphone
    4. Click headphone icon
    5. Select "CABLE Input" as speaker
    
    STEP 4: VERIFY SETUP
    ---------------------
    1. Open Sound Control Panel
    2. Go to Recording tab
    3. Right-click "CABLE Input" → Properties
    4. Go to Listen tab
    5. Check "Listen to this device"
    6. Select "CABLE Output" in dropdown
    7. Click Apply
    
    ✅ When you speak, you should hear yourself!
    """)

def print_linux_setup():
    """Print Linux audio setup instructions"""
    print("""
    =============================================
    🎤 LINUX AUDIO SETUP (PulseAudio)
    =============================================
    
    STEP 1: INSTALL PULSEAUDIO
    ---------------------------
    sudo apt-get install pulseaudio pavucontrol
    
    STEP 2: CREATE VIRTUAL MICROPHONE
    ---------------------------------
    1. Install module: 
       sudo apt-get install pulseaudio-module-loopback
    
    2. Load loopback module:
       pactl load-module module-loopback latency_msec=1
    
    STEP 3: CONFIGURE AUDIO
    ------------------------
    1. Run: pavucontrol
    2. Go to "Recording" tab
    3. Set "Loopback" as source for applications
    4. Go to "Playback" tab
    5. Set "Loopback" as output
    
    STEP 4: TELEGRAM SETUP
    -----------------------
    1. Join voice chat
    2. Set microphone to "Monitor of Built-in Audio"
    
    ✅ Your voice will be processed in real-time!
    """)

def print_mac_setup():
    """Print macOS audio setup instructions"""
    print("""
    =============================================
    🎤 macOS AUDIO SETUP (Soundflower/BlackHole)
    =============================================
    
    STEP 1: INSTALL BLACKHOLE
    --------------------------
    1. Download: https://existential.audio/blackhole/
    2. Install the .pkg file
    3. Restart computer
    
    STEP 2: CREATE MULTI-OUTPUT DEVICE
    -----------------------------------
    1. Open Audio MIDI Setup (Applications/Utilities)
    2. Click + button → Create Multi-Output Device
    3. Check both "Built-in Output" and "BlackHole 16ch"
    4. Right-click new device → Use This Device For Sound Output
    
    STEP 3: CONFIGURE TELEGRAM
    ---------------------------
    1. Join voice chat
    2. Set microphone to "BlackHole 16ch"
    
    STEP 4: TEST SETUP
    -------------------
    1. Open System Preferences → Sound
    2. Set Output to Multi-Output Device
    3. Set Input to BlackHole 16ch
    4. Speak and check if you hear yourself
    
    ✅ Voice processing is now ready!
    """)

def check_current_system():
    """Check and print current audio devices"""
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        print("\n📱 CURRENT AUDIO DEVICES:")
        print("-" * 40)
        
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"[INPUT {i}] {device['name']}")
            if device['max_output_channels'] > 0:
                print(f"[OUTPUT {i}] {device['name']}")
        
        print("-" * 40)
        
    except ImportError:
        print("⚠️ sounddevice not
