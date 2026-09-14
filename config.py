"""
Configuration and utilities for the Voice Assistant
"""
import os
from typing import Optional

class Config:
    """Application configuration"""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", False)
    
    # Audio settings
    SAMPLE_RATE = 16000
    RECORDING_DURATION = 5
    AUDIO_CHANNELS = 1
    
    # API settings
    OPENAI_MODEL = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS = 150
    
    # Google Cloud settings
    GOOGLE_LANGUAGE = "en-US"
    GOOGLE_VOICE_NAME = "en-US-Neural2-C"
    
    @classmethod
    def validate(cls) -> tuple[bool, Optional[str]]:
        """Validate configuration"""
        if not cls.OPENAI_API_KEY:
            return False, "OPENAI_API_KEY is not set"
        if not cls.GOOGLE_CREDENTIALS:
            return False, "GOOGLE_APPLICATION_CREDENTIALS is not set"
        return True, None


class AudioSettings:
    """Audio recording and playback settings"""
    SAMPLE_RATE = 16000
    CHANNELS = 1
    FORMAT = "float32"
    CHUNK_SIZE = 1024
    RECORDING_DURATION = 5
