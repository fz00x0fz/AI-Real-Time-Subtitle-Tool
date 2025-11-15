import io
import wave
import numpy as np
from abc import ABC, abstractmethod
from config import Config


class TranscriptionService(ABC):
    """Abstract base class for transcription services"""
    
    @abstractmethod
    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """Transcribe audio data to text"""
        pass
    
    def audio_to_wav_bytes(self, audio_data: np.ndarray, sample_rate: int) -> bytes:
        """Convert numpy audio data to WAV bytes"""
        # Normalize audio data to int16
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes (int16)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())
        
        wav_buffer.seek(0)
        return wav_buffer.read()


class OpenAITranscriptionService(TranscriptionService):
    """OpenAI Whisper API transcription service"""
    
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )
        self.model = Config.OPENAI_MODEL
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """Transcribe audio using OpenAI Whisper API"""
        try:
            # Convert to WAV bytes
            wav_bytes = self.audio_to_wav_bytes(audio_data, sample_rate)
            
            # Create a file-like object
            audio_file = io.BytesIO(wav_bytes)
            audio_file.name = "audio.wav"
            
            # Call OpenAI API
            response = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                response_format="text"
            )
            
            return response.strip() if response else ""
            
        except Exception as e:
            print(f"OpenAI transcription error: {e}")
            return ""


class AzureTranscriptionService(TranscriptionService):
    """Azure Speech Service transcription"""
    
    def __init__(self):
        import azure.cognitiveservices.speech as speechsdk
        
        self.speech_config = speechsdk.SpeechConfig(
            subscription=Config.AZURE_SPEECH_KEY,
            region=Config.AZURE_SPEECH_REGION
        )
        self.speech_config.speech_recognition_language = "zh-CN"  # Chinese, change as needed
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """Transcribe audio using Azure Speech Service"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            # Convert to WAV bytes
            wav_bytes = self.audio_to_wav_bytes(audio_data, sample_rate)
            
            # Create audio stream
            stream = speechsdk.audio.PushAudioInputStream()
            audio_config = speechsdk.audio.AudioConfig(stream=stream)
            
            # Create recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Push audio data
            stream.write(wav_bytes)
            stream.close()
            
            # Recognize
            result = speech_recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                return ""
            else:
                print(f"Azure recognition failed: {result.reason}")
                return ""
                
        except Exception as e:
            print(f"Azure transcription error: {e}")
            return ""


class AliyunTranscriptionService(TranscriptionService):
    """Aliyun Bailian (DashScope) transcription service"""
    
    def __init__(self):
        import requests
        self.api_key = Config.ALIYUN_API_KEY
        self.app_id = Config.ALIYUN_APP_ID
        self.endpoint = Config.ALIYUN_ENDPOINT
        self.model = Config.ALIYUN_MODEL
        self.session = requests.Session()
        
    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """Transcribe audio using Aliyun Bailian API"""
        try:
            import requests
            import base64
            
            # Convert to WAV bytes
            wav_bytes = self.audio_to_wav_bytes(audio_data, sample_rate)
            
            # Encode audio to base64
            audio_base64 = base64.b64encode(wav_bytes).decode('utf-8')
            
            # Prepare request headers - 使用正确的API格式
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Prepare request body - 使用阿里云百炼的标准格式
            payload = {
                'model': self.model,
                'input': {
                    'audio_data': audio_base64,
                    'format': 'wav',
                    'sample_rate': sample_rate,
                    'channel': 1
                },
                'parameters': {
                    'format': 'pcm'
                }
            }
            
            # If app_id is provided, include it in headers
            if self.app_id:
                headers['X-DashScope-AppId'] = self.app_id
            
            # Make API request
            response = self.session.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                
                # Debug: print response structure (first time only)
                if not hasattr(self, '_logged_response'):
                    print(f"[DEBUG] Aliyun API response structure: {result}")
                    self._logged_response = True
                
                # Parse result based on API response structure
                if 'output' in result:
                    output = result['output']
                    
                    # Method 1: Direct text field
                    if 'text' in output:
                        text = output['text'].strip()
                        if text:
                            return text
                    
                    # Method 2: Sentence field (single or multiple)
                    if 'sentence' in output:
                        sentences = output['sentence']
                        if isinstance(sentences, list):
                            text = ' '.join([s.get('text', '') for s in sentences]).strip()
                            if text:
                                return text
                        elif isinstance(sentences, dict):
                            text = sentences.get('text', '').strip()
                            if text:
                                return text
                    
                    # Method 3: Results array
                    if 'results' in output:
                        results = output['results']
                        if isinstance(results, list) and len(results) > 0:
                            text = results[0].get('text', '').strip()
                            if text:
                                return text
                    
                    # Method 4: Transcription field
                    if 'transcription' in output:
                        text = output['transcription'].strip()
                        if text:
                            return text
                
                # If output not found, check top-level fields
                if 'text' in result:
                    return result['text'].strip()
                
                # No text found
                print(f"[WARNING] No text found in Aliyun response: {result}")
                return ""
            else:
                error_msg = f"Aliyun API error: {response.status_code} - {response.text}"
                print(error_msg)
                return ""
                
        except Exception as e:
            print(f"Aliyun transcription error: {e}")
            import traceback
            traceback.print_exc()
            return ""


class LocalWhisperService(TranscriptionService):
    """Local Whisper model transcription (requires whisper package)"""
    
    def __init__(self):
        try:
            import whisper
            print("Loading local Whisper model (this may take a while)...")
            self.model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
            print("Whisper model loaded successfully")
        except ImportError:
            raise ImportError("Please install openai-whisper: pip install openai-whisper")
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """Transcribe audio using local Whisper model"""
        try:
            # Whisper expects float32 audio normalized to [-1, 1]
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Resample to 16kHz if needed (Whisper requirement)
            if sample_rate != 16000:
                # Simple resampling (for production, use librosa or scipy)
                audio_data = self._resample(audio_data, sample_rate, 16000)
            
            # Transcribe
            result = self.model.transcribe(audio_data, language="zh", fp16=False)
            return result["text"].strip()
            
        except Exception as e:
            print(f"Local Whisper transcription error: {e}")
            return ""
    
    def _resample(self, audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
        """Simple resampling (basic implementation)"""
        if orig_sr == target_sr:
            return audio
        
        duration = len(audio) / orig_sr
        target_length = int(duration * target_sr)
        
        # Linear interpolation
        indices = np.linspace(0, len(audio) - 1, target_length)
        return np.interp(indices, np.arange(len(audio)), audio).astype(np.float32)


def create_transcription_service() -> TranscriptionService:
    """Factory function to create appropriate transcription service"""
    service_type = Config.AI_SERVICE.lower()
    
    if service_type == 'openai':
        print("Using OpenAI Whisper API")
        return OpenAITranscriptionService()
    elif service_type == 'azure':
        print("Using Azure Speech Service")
        return AzureTranscriptionService()
    elif service_type == 'aliyun':
        print("Using Aliyun Bailian (DashScope) Service")
        return AliyunTranscriptionService()
    elif service_type == 'local_whisper':
        print("Using Local Whisper Model")
        return LocalWhisperService()
    else:
        raise ValueError(f"Unknown AI service: {service_type}. Choose from: openai, azure, aliyun, local_whisper")
