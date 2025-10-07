from typing import Optional
import os
from src.core.transcription_manager import TranscriptionManager
from src.config.whisper_config import get_default_whisper_config

try:
    from dotenv import load_dotenv  # optional convenience
    load_dotenv()
except Exception:
    pass


def transcribe_audio(audio_file_path: str, api_key: Optional[str] = None) -> str:
    """Transcribe audio using Whisper integration.

    Supports both local Whisper models and OpenAI API.
    Reads configuration from environment variables.
    """
    # Setup configuration
    config = get_default_whisper_config()
    
    # Override API key if provided
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        config["use_openai_api"] = True
    
    # Create transcription manager
    manager = TranscriptionManager({"whisper": config})
    
    # Perform transcription
    result = manager.transcribe_file(audio_file_path)
    
    # Return just the text for backward compatibility
    return result["text"]

