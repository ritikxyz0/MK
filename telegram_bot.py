"""
TELEGRAM BOT - Control Interface
Controls voice effects via Telegram bot
"""

import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import sys
import os

# Import config and voice processor
from config import API_ID, API_HASH, BOT_TOKEN, EFFECTS_CONFIG
from voice_enhancer import voice_processor

print("🤖 Telegram Voice Enhancer Bot Starting...")
print("=" * 50)

# Initialize Pyrogram client
app = Client(
    "voice_enhancer_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===================== KEYBOARD BUTTONS =====================
effect_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔥 HIGE", callback_data="effect_hige"),
        InlineKeyboardButton("⚡ ULTRA", callback_data="effect_ultra")
    ],
    [
        InlineKeyboardButton("🎵 BASS", callback_data="effect_bass"),
        InlineKeyboardButton("✨ CLEAR", callback_data="effect_clear")
    ],
    [
        InlineKeyboardButton("🤖 ROBOT", callback_data="effect_robot"),
        InlineKeyboardButton("🔈 NORMAL", callback_data="effect_normal")
    ]
])

gain_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("1.0x", callback_data="gain_1.0"),
        InlineKeyboardButton("1.5x", callback_data="gain_1.5"),
        InlineKeyboardButton("2.0x", callback_data="gain_2.0")
    ],
    [
        InlineKeyboardButton("2.5x", callback_data="gain_2.5"),
        InlineKeyboardButton("3.0x", callback_data="gain_3.0"),
        InlineKeyboardButton("3.5x", callback_data="gain_3.5")
    ],
    [
        InlineKeyboardButton("4.0x", callback_data="gain_4.0"),
        InlineKeyboardButton("4.5x", callback_data="gain_4.5"),
        InlineKeyboardButton("5.0x", callback_data="gain_5.0")
    ]
])

main_menu_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🎛️ Effects", callback_data="menu_effects"),
        InlineKeyboardButton("🔊 Gain", callback_data="menu_gain")
    ],
    [
        InlineKeyboardButton("▶️ Start Audio", callback_data="start_audio"),
        InlineKeyboardButton("⏹️ Stop Audio", callback_data="stop_audio")
    ],
    [
        InlineKeyboardButton("📊 Status", callback_data="menu_status")
    ]
])

# ===================== COMMAND HANDLERS =====================
@app.on_message(filters.command("start"))
async def start_command(client, message):
    """Handle /start command"""
    welcome_text = """
    🎤 **VOICE ENHANCER BOT** 🎤
    
    **Apni awaaz ko banayein POWERFUL!**
    
    **Features:**
    • 🔥 HIGE - High gain + bass
    • ⚡ ULTRA - Extreme gain
    • 🎵 BASS - Deep bass boost
    • ✨ CLEAR - Clear voice
    • 🤖 ROBOT - Robot voice effect
    
    **Commands:**
    /menu - Main control menu
    /effects - Voice effects
    /gain [1-5] - Set volume (e.g., /gain 3.5)
    /startaudio - Start voice enhancement
    /stopaudio - Stop voice enhancement
    /status - Current settings
    
    **Setup:**
    1. Install Virtual Audio Cable (VB-Cable)
    2. Set VB-Cable as default microphone
    3. Use /startaudio to begin
    4. Join Telegram voice chat
    5. Select VB-Cable as microphone
    
    **Note:** Ye bot real-time mein aapki awaaz enhance karega!
    """
    await message.reply(welcome_text, reply_markup=main_menu_buttons)

@app.on_message(filters.command("menu"))
async def menu_command(client, message):
    """Show main menu"""
    await message.reply("🎛️ **Main Control Menu:**", reply_markup=main_menu_buttons)

@app.on_message(filters.command("effects"))
async def effects_command(client, message):
    """Show effects menu"""
    await message.reply(
        "🎚️ **Select Voice Effect:**\n\n"
        "• 🔥 HIGE: High gain + bass boost\n"
        "• ⚡ ULTRA: Extreme gain with compression\n"
        "• 🎵 BASS: Deep bass enhancement\n"
        "• ✨ CLEAR: Clear voice with noise reduction\n"
        "• 🤖 ROBOT: Robot/electronic effect\n"
        "• 🔈 NORMAL: Original voice",
        reply_markup=effect_buttons
    )

@app.on_message(filters.command("gain"))
async def gain_command(client, message):
    """Set gain from command"""
    try:
        args = message.text.split()
        if len(args) > 1:
            gain = float(args[1])
            if 0.1 <= gain <= 5.0:
                if voice_processor.change_gain(gain):
                    await message.reply(f"✅ Gain set to: **{gain}x**")
                else:
                    await message.reply("❌ Failed to set gain")
            else:
                await message.reply("⚠️ Gain must be between 0.1 and 5.0")
        else:
            await message.reply(
                "🔊 **Select Volume Gain:**\n"
                "Or use: /gain [number]\n"
                "Example: /gain 3.5",
                reply_markup=gain_buttons
            )
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

@app.on_message(filters.command("startaudio"))
async def start_audio_command(client, message):
    """Start audio processing"""
    try:
        # Start in background thread
        def start_processing():
            voice_processor.start_processing()
        
        thread = threading.Thread(target=start_processing, daemon=True)
        thread.start()
        
        await message.reply(
            "✅ **Voice processing STARTED!**\n\n"
            "**Ab aapko:**\n"
            "1. Virtual Audio Cable (VB-Cable) install karna hai\n"
            "2. Default microphone VB-Cable set karna hai\n"
            "3. Telegram voice chat join karna hai\n"
            "4. Microphone select karte waqt VB-Cable choose karna hai\n\n"
            "📱 Use /effects to change voice style!"
        )
    except Exception as e:
        await message.reply(f"❌ Error starting audio: {str(e)}")

@app.on_message(filters.command("stopaudio"))
async def stop_audio_command(client, message):
    """Stop audio processing"""
    if voice_processor.stop_processing():
        await message.reply("✅ **Voice processing STOPPED!**")
    else:
        await message.reply("⚠️ Audio processing was not running")

@app.on_message(filters.command("status"))
async def status_command(client, message):
    """Show current status"""
    status = voice_processor.get_status()
    
    status_text = f"""
    ⚙️ **CURRENT SETTINGS:**
    
    • **Effect:** {status['effect_name']}
    • **Gain:** {status['gain']}x
    • **Status:** {'🟢 RUNNING' if status['is_processing'] else '🔴 STOPPED'}
    • **Sample Rate:** {status['sample_rate']} Hz
    
    **Next Steps:**
    /effects - Change voice effect
    /gain - Adjust volume
    /startaudio - Start processing
    /stopaudio - Stop processing
    """
    await message.reply(status_text, reply_markup=main_menu_buttons)

# ===================== CALLBACK HANDLERS =====================
@app.on_callback_query()
async def handle_callback(client, callback_query):
    """Handle all button clicks"""
    data = callback_query.data
    
    try:
        if data.startswith("effect_"):
            # Handle effect selection
            effect = data.split("_")[1]
            if voice_processor.change_effect(effect):
                effect_name = EFFECTS_CONFIG.get(effect, {}).get("name", effect.upper())
                await callback_query.answer(f"✅ Effect: {effect_name}")
                await callback_query.message.edit_text(
                    f"🎛️ **Effect Selected:** {effect_name}\n"
                    f"🔊 **Gain:** {voice_processor.current_gain}x\n\n"
                    "📱 Select another effect:",
                    reply_markup=effect_buttons
                )
            else:
                await callback_query.answer("❌ Failed to change effect")
        
        elif data.startswith("gain_"):
            # Handle gain selection
            gain = float(data.split("_")[1])
            if voice_processor.change_gain(gain):
                await callback_query.answer(f"✅ Gain: {gain}x")
                await callback_query.message.edit_text(
                    f"🔊 **Gain Set:** {gain}x\n"
                    f"🎛️ **Effect:** {voice_processor.current_effect.upper()}\n\n"
                    "📱 Select another gain level:",
                    reply_markup=gain_buttons
                )
            else:
                await callback_query.answer("❌ Invalid gain value")
        
        elif data == "menu_effects":
            # Show effects menu
            await callback_query.answer("Opening effects menu...")
            await callback_query.message.edit_text(
                "🎚️ **Select Voice Effect:**",
                reply_markup=effect_buttons
            )
        
        elif data == "menu_gain":
            # Show gain menu
            await callback_query.answer("Opening gain menu...")
            await callback_query.message.edit_text(
                "🔊 **Select Volume Gain:**",
                reply_markup=gain_buttons
            )
        
        elif data == "start_audio":
            # Start audio processing
            await callback_query.answer("Starting audio processing...")
            
            def start_in_thread():
                voice_processor.start_processing()
            
            thread = threading.Thread(target=start_in_thread, daemon=True)
            thread.start()
            
            await callback_query.message.edit_text(
                "✅ **Voice processing STARTED!**\n\n"
                "**Instructions:**\n"
                "1. Make sure VB-Cable is installed\n"
                "2. Set VB-Cable as default mic\n"
                "3. Join Telegram voice chat\n"
                "4. Select VB-Cable as microphone\n\n"
                "📱 Use /effects to change voice style!",
                reply_markup=main_menu_buttons
            )
        
        elif data == "stop_audio":
            # Stop audio processing
            await callback_query.answer("Stopping audio processing...")
            
            if voice_processor.stop_processing():
                await callback_query.message.edit_text(
                    "⏹️ **Voice processing STOPPED!**\n\n"
                    "Use /startaudio to begin again",
                    reply_markup=main_menu_buttons
                )
            else:
                await callback_query.answer("Audio was not running")
        
        elif data == "menu_status":
            # Show status
            await callback_query.answer("Getting status...")
            status = voice_processor.get_status()
            
            status_text = f"""
            📊 **STATUS REPORT:**
            
            • **Effect:** {status['effect_name']}
            • **Gain:** {status['gain']}x
            • **Status:** {'🟢 RUNNING' if status['is_processing'] else '🔴 STOPPED'}
            • **Sample Rate:** {status['sample_rate']} Hz
            
            **Controls:**
            Use buttons below to manage
            """
            await callback_query.message.edit_text(
                status_text,
                reply_markup=main_menu_buttons
            )
        
        elif data == "menu":
            # Return to main menu
            await callback_query.answer("Opening main menu...")
            await callback_query.message.edit_text(
                "🎛️ **Main Control Menu:**",
                reply_markup=main_menu_buttons
            )
    
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}")
        print(f"Callback error: {e}")

# ===================== ERROR HANDLING =====================
@app.on_message()
async def handle_all_messages(client, message):
    """Handle unknown commands"""
    if message.text and message.text.startswith("/"):
        await message.reply(
            "❌ Unknown command!\n\n"
            "**Available commands:**\n"
            "/start - Show help\n"
            "/menu - Main menu\n"
            "/effects - Voice effects\n"
            "/gain - Volume control\n"
            "/startaudio - Start processing\n"
            "/stopaudio - Stop processing\n"
            "/status - Current settings"
        )

# ===================== MAIN FUNCTION =====================
def main():
    """Main function to run the bot"""
    print("=" * 50)
    print("🎤 VOICE ENHANCER BOT")
    print("=" * 50)
    print(f"API ID: {API_ID}")
    print(f"Effect: {voice_processor.current_effect.upper()}")
    print(f"Gain: {voice_processor.current_gain}x")
    print("=" * 50)
    print("\n📱 Send /start to your bot in Telegram")
    print("💡 Use /startaudio to begin voice enhancement")
    print("=" * 50)
    
    try:
        # Run the bot
        app.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
        voice_processor.stop_processing()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
