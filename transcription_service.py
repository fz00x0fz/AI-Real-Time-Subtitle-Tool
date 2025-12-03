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
    """Aliyun Bailian (DashScope) transcription service
    
    基于官方示例: example/dashscope/call_dashscope_paraformer-realtime-v2.md
    """
    
    def __init__(self):
        try:
            import dashscope
            from dashscope.audio.asr import Recognition
            from http import HTTPStatus
            
            # 设置API Key（参考官方示例）
            dashscope.api_key = Config.ALIYUN_API_KEY
            
            self.model = Config.ALIYUN_MODEL
            self.sample_rate = Config.SAMPLE_RATE
            self.Recognition = Recognition
            self.HTTPStatus = HTTPStatus
            self.dashscope = dashscope
            
            # 性能指标记录
            self._first_call = True
            self._total_calls = 0
            self._success_calls = 0
            
            print(f"[Aliyun] Initialized with model: {self.model}")
            print(f"[Aliyun] Sample rate: {self.sample_rate} Hz")
            
        except ImportError as e:
            print("=" * 60)
            print("[ERROR] dashscope SDK未安装")
            print("=" * 60)
            print()
            print("请安装阿里云DashScope SDK:")
            print("  pip install dashscope")
            print()
            print("=" * 60)
            raise
        
    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """Transcribe audio using Aliyun DashScope SDK
        
        参考官方示例实现，支持以下特性：
        - paraformer-realtime-v2: 支持language_hints（中英文混合）
        - fun-asr-realtime-2025-11-07: 最新模型
        """
        self._total_calls += 1
        
        try:
            import tempfile
            import os
            
            # Convert to WAV bytes
            wav_bytes = self.audio_to_wav_bytes(audio_data, sample_rate)
            
            # 创建临时文件保存音频数据
            # 使用with语句确保文件正确关闭
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(wav_bytes)
                temp_file_path = temp_file.name
            
            try:
                # 根据模型选择是否使用language_hints
                # 参考官方示例："language_hints"只支持paraformer-realtime-v2模型
                if self.model == 'paraformer-realtime-v2':
                    recognition = self.Recognition(
                        model=self.model,
                        format='wav',
                        sample_rate=sample_rate,
                        language_hints=['zh', 'en'],  # 中英文混合识别
                        callback=None
                    )
                else:
                    # 其他模型（如fun-asr-realtime-2025-11-07）不使用language_hints
                    recognition = self.Recognition(
                        model=self.model,
                        format='wav',
                        sample_rate=sample_rate,
                        callback=None
                    )
                
                # 调用识别API（参考官方示例）
                result = recognition.call(temp_file_path)
                
                # 检查识别结果（参考官方示例的错误处理）
                if result.status_code == self.HTTPStatus.OK:
                    self._success_calls += 1
                    
                    # 获取识别文本（使用官方推荐的get_sentence()方法）
                    text = result.get_sentence()
                    
                    # 打印性能指标（参考官方示例的Metric输出）
                    if self._first_call:
                        print(
                            f'[Aliyun Metric] requestId: {recognition.get_last_request_id()}, '
                            f'first package delay: {recognition.get_first_package_delay()}ms, '
                            f'last package delay: {recognition.get_last_package_delay()}ms'
                        )
                        self._first_call = False
                    
                    # 返回识别结果
                    if text:
                        return text.strip()
                    else:
                        # 无识别结果（可能是静音或噪音）
                        return ""
                else:
                    # 识别失败，输出错误信息（参考官方示例）
                    print(f'[Aliyun Error] {result.status_code}: {result.message}')
                    return ""
                    
            finally:
                # 删除临时文件，确保资源清理
                try:
                    os.unlink(temp_file_path)
                except Exception as cleanup_error:
                    # 忽略删除文件时的错误
                    pass
                
        except Exception as e:
            print(f"[Aliyun] Transcription error: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def get_stats(self):
        """获取统计信息"""
        if self._total_calls > 0:
            success_rate = (self._success_calls / self._total_calls) * 100
            return {
                'total_calls': self._total_calls,
                'success_calls': self._success_calls,
                'success_rate': f'{success_rate:.1f}%'
            }
        return None


class LocalWhisperService(TranscriptionService):
    """Local Whisper model transcription (requires whisper package)"""
    
    def __init__(self):
        self.model = None
        try:
            import whisper
            print("Loading local Whisper model (this may take a while)...")
            self.model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
            print("Whisper model loaded successfully")
        except ImportError as e:
            print("=" * 60)
            print("[WARNING] 本地Whisper模型未安装")
            print("=" * 60)
            print()
            print("请选择以下方式之一安装:")
            print()
            print("方式1: 通过图形界面安装（推荐）")
            print("  1. 点击主窗口的⚙按钮打开配置")
            print("  2. 点击'安装本地模型'按钮")
            print("  3. 等待安装完成")
            print()
            print("方式2: 手动安装")
            print("  pip install openai-whisper")
            print()
            print("=" * 60)
            # 不抛出异常，让程序继续运行
        except Exception as e:
            print(f"加载Whisper模型时出错: {e}")
            print("请尝试重新安装: pip install openai-whisper")
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """Transcribe audio using local Whisper model"""
        # 检查模型是否已加载
        if self.model is None:
            return "[本地模型未安装，请在配置中安装]"
        
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
