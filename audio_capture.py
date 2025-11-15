import sounddevice as sd
import numpy as np
import queue
import threading
from config import Config


class AudioCapture:
    """Captures system audio on Windows using WASAPI loopback"""
    
    def __init__(self, callback=None):
        self.callback = callback
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.stream = None
        self.sample_rate = Config.SAMPLE_RATE
        self.chunk_duration = Config.CHUNK_DURATION
        self.buffer = []
        
    def list_devices(self):
        """List all available audio devices"""
        devices = sd.query_devices()
        print("\n=== Available Audio Devices ===")
        for idx, device in enumerate(devices):
            print(f"{idx}: {device['name']}")
            print(f"   Max Input Channels: {device['max_input_channels']}")
            print(f"   Max Output Channels: {device['max_output_channels']}")
            print(f"   Default Sample Rate: {device['default_samplerate']}")
        return devices
    
    def get_loopback_device(self):
        """Get Windows WASAPI loopback device for system audio capture"""
        devices = sd.query_devices()
        
        # Look for loopback devices (usually have "Stereo Mix" or similar in name)
        # On Windows with WASAPI, we need to use the default output device as input
        default_output = sd.query_devices(kind='output')
        
        print(f"\nUsing default output device for loopback: {default_output['name']}")
        return default_output['index']
    
    def audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream"""
        if status:
            print(f"Audio status: {status}")
        
        # Convert to mono if stereo
        if len(indata.shape) > 1:
            audio_data = np.mean(indata, axis=1)
        else:
            audio_data = indata.copy()
        
        self.buffer.extend(audio_data)
        
        # When buffer reaches chunk duration, process it
        chunk_size = int(self.sample_rate * self.chunk_duration)
        if len(self.buffer) >= chunk_size:
            chunk = np.array(self.buffer[:chunk_size], dtype=np.float32)
            self.buffer = self.buffer[chunk_size:]
            
            # Put chunk in queue for processing
            self.audio_queue.put(chunk)
            
            # Call callback if provided
            if self.callback:
                self.callback(chunk)
    
    def start_capture(self, device_index=None):
        """Start capturing audio"""
        if self.is_recording:
            print("Already recording")
            return
        
        try:
            # Get device index
            if device_index is None:
                device_index = Config.AUDIO_DEVICE_INDEX
                if device_index == -1:
                    device_index = self.get_loopback_device()
            
            print(f"\nStarting audio capture on device {device_index}")
            print(f"Sample rate: {self.sample_rate} Hz")
            print(f"Chunk duration: {self.chunk_duration} seconds")
            
            # Create input stream
            # For Windows WASAPI loopback, we need to use specific hostapi
            self.stream = sd.InputStream(
                device=device_index,
                channels=1,
                samplerate=self.sample_rate,
                callback=self.audio_callback,
                blocksize=int(self.sample_rate * 0.1)  # 100ms blocks
            )
            
            self.stream.start()
            self.is_recording = True
            print("Audio capture started successfully")
            
        except Exception as e:
            print(f"Error starting audio capture: {e}")
            print("\nTrying alternative method with default input device...")
            try:
                # Fallback to default input device
                self.stream = sd.InputStream(
                    channels=1,
                    samplerate=self.sample_rate,
                    callback=self.audio_callback,
                    blocksize=int(self.sample_rate * 0.1)
                )
                self.stream.start()
                self.is_recording = True
                print("Audio capture started with default input device")
            except Exception as e2:
                print(f"Error with fallback method: {e2}")
                raise
    
    def stop_capture(self):
        """Stop capturing audio"""
        if not self.is_recording:
            return
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        self.is_recording = False
        self.buffer = []
        print("Audio capture stopped")
    
    def get_audio_chunk(self, timeout=1):
        """Get next audio chunk from queue"""
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def __del__(self):
        """Cleanup"""
        self.stop_capture()
