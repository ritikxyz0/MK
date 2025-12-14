"""
VOICE ENHANCER - Core Audio Processing
Real-time voice effects processing
"""

import numpy as np
from scipy import signal
import sounddevice as sd
import threading
import time
from config import SAMPLE_RATE, EFFECTS_CONFIG

class VoiceProcessor:
    """
    Real-time voice processing class
    Applies effects like HIGE, ULTRA, BASS BOOST to microphone input
    """
    
    def __init__(self):
        self.current_effect = "hige"
        self.current_gain = 2.5
        self.is_processing = False
        self.stream = None
        self.processing_thread = None
        
        # Audio buffers
        self.input_buffer = []
        self.output_buffer = []
        
        # Effect parameters
        self.setup_filters()
        
        print("🎤 Voice Processor Initialized")
        print(f"Default Effect: {self.current_effect.upper()}")
        print(f"Default Gain: {self.current_gain}x")
    
    def setup_filters(self):
        """Setup audio filters for effects"""
        # Low-pass filter for bass
        self.bass_sos = signal.butter(
            4, 150, 'lowpass', fs=SAMPLE_RATE, output='sos'
        )
        
        # High-pass filter for clarity
        self.treble_sos = signal.butter(
            4, 3000, 'highpass', fs=SAMPLE_RATE, output='sos'
        )
        
        # Band-pass filter for voice
        self.voice_sos = signal.butter(
            4, [300, 3400], 'bandpass', fs=SAMPLE_RATE, output='sos'
        )
        
        # Robot effect filter
        self.robot_sos = signal.butter(
            6, [500, 2500], 'bandpass', fs=SAMPLE_RATE, output='sos'
        )
    
    def apply_hige_effect(self, audio):
        """Apply HIGE (High Gain + Bass) effect"""
        # Boost volume
        audio = audio * 2.5
        
        # Add bass
        bass = signal.sosfilt(self.bass_sos, audio)
        audio = audio + (bass * 0.7)
        
        # Add slight treble
        treble = signal.sosfilt(self.treble_sos, audio)
        audio = audio + (treble * 0.3)
        
        return audio
    
    def apply_ultra_effect(self, audio):
        """Apply ULTRA (Extreme Gain) effect"""
        # Extreme volume boost
        audio = audio * 3.5
        
        # Compression to prevent clipping
        audio = np.tanh(audio * 1.5) / 1.5
        
        # Enhance bass and treble
        bass = signal.sosfilt(self.bass_sos, audio) * 0.9
        treble = signal.sosfilt(self.treble_sos, audio) * 0.5
        audio = audio + bass + treble
        
        return audio
    
    def apply_bass_effect(self, audio):
        """Apply BASS BOOST effect"""
        # Moderate volume
        audio = audio * 2.0
        
        # Heavy bass boost
        bass = signal.sosfilt(self.bass_sos, audio)
        audio = audio + (bass * 1.2)
        
        # Reduce treble
        audio = signal.sosfilt(self.treble_sos, audio) * 0.1
        
        return audio
    
    def apply_clear_effect(self, audio):
        """Apply CLEAR VOICE effect"""
        # Focus on voice frequencies
        audio = signal.sosfilt(self.voice_sos, audio)
        
        # Volume boost
        audio = audio * 2.2
        
        # Enhance clarity
        treble = signal.sosfilt(self.treble_sos, audio) * 0.8
        audio = audio + treble
        
        return audio
    
    def apply_robot_effect(self, audio):
        """Apply ROBOT VOICE effect"""
        # Robot-like bandpass
        audio = signal.sosfilt(self.robot_sos, audio)
        
        # Volume boost
        audio = audio * 2.5
        
        # Bitcrusher effect for robotic sound
        step = 0.05
        audio = np.round(audio / step) * step
        
        return audio
    
    def process_audio(self, audio_data):
        """Main audio processing function"""
        # Convert to float for processing
        audio = audio_data.astype(np.float32) / 32768.0
        
        # Apply selected effect
        if self.current_effect == "hige":
            audio = self.apply_hige_effect(audio)
        elif self.current_effect == "ultra":
            audio = self.apply_ultra_effect(audio)
        elif self.current_effect == "bass":
            audio = self.apply_bass_effect(audio)
        elif self.current_effect == "clear":
            audio = self.apply_clear_effect(audio)
        elif self.current_effect == "robot":
            audio = self.apply_robot_effect(audio)
        elif self.current_effect == "normal":
            # Normal voice (just gain)
            audio = audio * self.current_gain
        
        # Apply final gain
        audio = audio * self.current_gain
        
        # Prevent clipping
        audio = np.clip(audio, -0.99, 0.99)
        
        # Convert back to int16
        audio = (audio * 32767.0).astype(np.int16)
        
        return audio
    
    def audio_callback(self, indata, outdata, frames, time_info, status):
        """SoundDevice callback for real-time processing"""
        if status:
            print(f"Audio Status: {status}")
        
        # Process incoming audio
        if indata is not None and len(indata) > 0:
            processed = self.process_audio(indata[:, 0])
            
            # Output processed audio
            outdata[:, 0] = processed.astype(np.float32) / 32768.0
            
            # If stereo output, duplicate to right channel
            if outdata.shape[1] > 1:
                outdata[:, 1] = outdata[:, 0]
    
    def start_processing(self):
        """Start real-time audio processing"""
        if self.is_processing:
            print("⚠️ Processing already running!")
            return False
        
        try:
            print("🚀 Starting voice processing...")
            print(f"Effect: {self.current_effect.upper()}")
            print(f"Gain: {self.current_gain}x")
            
            # Start audio stream
            self.stream = sd.Stream(
                callback=self.audio_callback,
                channels=1,
                samplerate=SAMPLE_RATE,
                blocksize=1024,
                dtype='float32'
            )
            
            self.stream.start()
            self.is_processing = True
            
            print("✅ Voice processing ACTIVE!")
            print("▶️ Speak into your microphone...")
            print("🔧 Use Telegram bot to change effects")
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting audio processing: {e}")
            return False
    
    def stop_processing(self):
        """Stop audio processing"""
        if self.stream and self.is_processing:
            print("🛑 Stopping voice processing...")
            self.stream.stop()
            self.stream.close()
            self.is_processing = False
            print("✅ Processing stopped")
            return True
        return False
    
    def change_effect(self, effect_name):
        """Change current voice effect"""
        if effect_name in EFFECTS_CONFIG:
            self.current_effect = effect_name
            self.current_gain = EFFECTS_CONFIG[effect_name]["gain"]
            
            print(f"✅ Effect changed to: {EFFECTS_CONFIG[effect_name]['name']}")
            print(f"📊 Gain: {self.current_gain}x")
            
            return True
        else:
            print(f"❌ Invalid effect: {effect_name}")
            return False
    
    def change_gain(self, gain_value):
        """Change volume gain"""
        if 0.1 <= gain_value <= 5.0:
            self.current_gain = gain_value
            print(f"✅ Gain changed to: {gain_value}x")
            return True
        else:
            print("❌ Gain must be between 0.1 and 5.0")
            return False
    
    def get_status(self):
        """Get current processing status"""
        return {
            "effect": self.current_effect,
            "effect_name": EFFECTS_CONFIG.get(self.current_effect, {}).get("name", "Unknown"),
            "gain": self.current_gain,
            "is_processing": self.is_processing,
            "sample_rate": SAMPLE_RATE
        }

# Global instance
voice_processor = VoiceProcessor()
