import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal

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
        
        # Connect signals
        self.window.start_clicked.connect(self.start_capture)
        self.window.stop_clicked.connect(self.stop_capture)
        
    def initialize(self):
        """Initialize services"""
        try:
            print("\n=== Initializing AI Subtitle Tool ===")
            
            # Validate configuration
            Config.validate()
            print("✓ Configuration validated")
            
            # Initialize audio capture
            self.audio_capture = AudioCapture()
            print("✓ Audio capture initialized")
            
            # List available audio devices
            self.audio_capture.list_devices()
            
            # Initialize transcription service
            self.transcription_service = create_transcription_service()
            print("✓ Transcription service initialized")
            
            # Initialize transcription worker
            self.transcription_worker = TranscriptionWorker(
                self.audio_capture,
                self.transcription_service
            )
            self.transcription_worker.subtitle_updated.connect(
                self.window.update_subtitle
            )
            print("✓ Transcription worker initialized")
            
            print("\n=== Initialization Complete ===\n")
            return True
            
        except Exception as e:
            error_msg = f"初始化失败: {str(e)}\n\n请检查配置文件和API密钥。"
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
        
    def cleanup(self):
        """Cleanup resources"""
        print("\nCleaning up...")
        self.stop_capture()


def main():
    """Main entry point"""
    app = AISubtitleApp()
    
    try:
        exit_code = app.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        exit_code = 0
    finally:
        app.cleanup()
        
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
