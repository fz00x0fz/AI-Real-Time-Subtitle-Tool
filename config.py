import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # AI Service Configuration
    AI_SERVICE = os.getenv('AI_SERVICE', 'openai')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'whisper-1')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    
    # Azure Speech Configuration
    AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY', '')
    AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION', 'eastus')
    
    # Aliyun Bailian Configuration
    ALIYUN_API_KEY = os.getenv('ALIYUN_API_KEY', '')
    # 支持的模型: paraformer-realtime-v2, fun-asr-realtime-2025-11-07
    ALIYUN_MODEL = os.getenv('ALIYUN_MODEL', 'paraformer-realtime-v2')
    
    # Audio Settings
    SAMPLE_RATE = int(os.getenv('SAMPLE_RATE', 16000))
    CHUNK_DURATION = int(os.getenv('CHUNK_DURATION', 3))  # seconds
    AUDIO_DEVICE_INDEX = int(os.getenv('AUDIO_DEVICE_INDEX', -1))
    
    # UI Settings
    WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', 800))
    WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', 120))
    WINDOW_OPACITY = float(os.getenv('WINDOW_OPACITY', 0.85))
    FONT_SIZE = int(os.getenv('FONT_SIZE', 24))
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if cls.AI_SERVICE == 'openai' and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI service")
        if cls.AI_SERVICE == 'azure' and (not cls.AZURE_SPEECH_KEY or not cls.AZURE_SPEECH_REGION):
            raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required when using Azure service")
        if cls.AI_SERVICE == 'aliyun' and not cls.ALIYUN_API_KEY:
            raise ValueError("ALIYUN_API_KEY is required when using Aliyun service")
        return True
