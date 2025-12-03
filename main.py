import sys
import threading
import time
import signal
import atexit
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from config import Config
from audio_capture import AudioCapture
from transcription_service import create_transcription_service
from subtitle_window import SubtitleWindow


class TranscriptionWorker(QObject):
    """Worker thread for audio transcription"""
    
    # Signal to update subtitle
    subtitle_updated = pyqtSignal(str)
    
    def __init__(self, audio_capture, transcription_service):
        super().__init__()
        self.audio_capture = audio_capture
        self.transcription_service = transcription_service
        self.running = False
        self.thread = None
        
    def start(self):
        """Start transcription worker"""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._process_audio, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop transcription worker"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
            
    def _process_audio(self):
        """Process audio chunks and transcribe"""
        print("Transcription worker started")
        
        while self.running:
            try:
                # Get audio chunk from queue
                audio_chunk = self.audio_capture.get_audio_chunk(timeout=0.5)
                
                if audio_chunk is not None:
                    print(f"Processing audio chunk: {len(audio_chunk)} samples")
                    
                    # Transcribe audio
                    text = self.transcription_service.transcribe(
                        audio_chunk, 
                        Config.SAMPLE_RATE
                    )
                    
                    # Emit signal with transcribed text
                    if text and text.strip():
                        print(f"Transcription: {text}")
                        self.subtitle_updated.emit(text)
                    else:
                        print("No speech detected in audio chunk")
                        
            except Exception as e:
                print(f"Error in transcription worker: {e}")
                time.sleep(0.1)
                
        print("Transcription worker stopped")


class AISubtitleApp:
    """Main application class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = SubtitleWindow()
        self.audio_capture = None
        self.transcription_service = None
        self.transcription_worker = None
        self._cleanup_done = False
        
        # Connect signals
        self.window.start_clicked.connect(self.start_capture)
        self.window.stop_clicked.connect(self.stop_capture)
        self.app.aboutToQuit.connect(self.cleanup)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Register cleanup at exit
        atexit.register(self.cleanup)
        
        # Setup timer to handle Ctrl+C in console
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: None)
        self.timer.start(500)
        
    def initialize(self):
        """Initialize services"""
        try:
            print("\n=== Initializing AI Subtitle Tool ===")
            
            # Validate configuration
            Config.validate()
            print("[OK] Configuration validated")
            
            # Initialize audio capture
            self.audio_capture = AudioCapture()
            print("[OK] Audio capture initialized")
            
            # List available audio devices
            self.audio_capture.list_devices()
            
            # Initialize transcription service
            self.transcription_service = create_transcription_service()
            print("[OK] Transcription service initialized")
            
            # Initialize transcription worker
            self.transcription_worker = TranscriptionWorker(
                self.audio_capture,
                self.transcription_service
            )
            self.transcription_worker.subtitle_updated.connect(
                self.window.update_subtitle
            )
            print("[OK] Transcription worker initialized")
            
            print("\n=== Initialization Complete ===\n")
            return True
            
        except Exception as e:
            error_msg = f"Initialization failed: {str(e)}\n\nPlease check your configuration file and API key."
            print(f"Error: {error_msg}")
            QMessageBox.critical(None, "初始化错误", error_msg)
            return False
            
    def start_capture(self):
        """Start audio capture and transcription"""
        try:
            print("\n=== Starting Audio Capture ===")
            
            # Start audio capture
            self.audio_capture.start_capture()
            
            # Start transcription worker
            self.transcription_worker.start()
            
            print("=== Audio Capture Started ===\n")
            
        except Exception as e:
            error_msg = f"启动失败: {str(e)}"
            print(f"Error: {error_msg}")
            QMessageBox.warning(self.window, "启动错误", error_msg)
            self.window.on_stop_clicked()
            
    def stop_capture(self):
        """Stop audio capture and transcription"""
        try:
            print("\n=== Stopping Audio Capture ===")
            
            # Stop transcription worker
            if self.transcription_worker:
                self.transcription_worker.stop()
            
            # Stop audio capture
            if self.audio_capture:
                self.audio_capture.stop_capture()
            
            print("=== Audio Capture Stopped ===\n")
            
        except Exception as e:
            print(f"Error stopping capture: {e}")
            
    def run(self):
        """Run the application"""
        if not self.initialize():
            return 1
            
        self.window.show()
        return self.app.exec_()
        
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown"""
        print(f"\nReceived signal {signum}, shutting down...")
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Cleanup resources"""
        if self._cleanup_done:
            return
        
        self._cleanup_done = True
        print("\nCleaning up...")
        
        try:
            # Stop timer
            if hasattr(self, 'timer'):
                self.timer.stop()
            
            # Stop capture
            self.stop_capture()
            
            # Force cleanup of audio stream
            if self.audio_capture and hasattr(self.audio_capture, 'stream'):
                if self.audio_capture.stream:
                    try:
                        self.audio_capture.stream.abort()
                    except:
                        pass
            
            # Give threads time to finish
            time.sleep(0.5)
            
            print("Cleanup complete")
        except Exception as e:
            print(f"Error during cleanup: {e}")


def main():
    """Main entry point"""
    app = None
    exit_code = 0
    
    try:
        app = AISubtitleApp()
        exit_code = app.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        exit_code = 0
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        exit_code = 1
    finally:
        if app:
            app.cleanup()
        # Force exit to ensure shell terminates
        print("Exiting...")
        
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
