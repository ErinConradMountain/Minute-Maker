"""
Whisper transcription service for audio processing.
Handles audio file transcription using OpenAI's Whisper model.
"""

import os
import tempfile
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import httpx

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..utils.audio_utils import validate_audio_file, convert_audio_format


logger = logging.getLogger(__name__)


class WhisperService:
    """Service for transcribing audio using Whisper models."""
    
    def __init__(
        self,
        model_name: str = "base",
        use_openai_api: bool = False,
        provider: Optional[str] = None,
        api_base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_endpoint: Optional[str] = None,
    ):
        """
        Initialize Whisper service.
        
        Args:
            model_name: Local model size (tiny, base, small, medium, large)
            use_openai_api: Whether to use OpenAI's API instead of local model
        """
        self.model_name = model_name
        self.use_openai_api = use_openai_api
        self.provider = (provider or ("openai" if use_openai_api else "local")).lower()
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.api_endpoint = api_endpoint or "/v1/transcriptions"
        self.model = None
        self.openai_client = None
        
        if self.provider == "openai":
            self._setup_openai_client()
        elif self.provider == "local":
            # Defer loading the local model until first use to make testing easier
            self.model = None
        elif self.provider == "whisper_api":
            self._setup_third_party_client()
        else:
            raise ValueError(f"Unknown Whisper provider: {self.provider}")
    
    def _setup_openai_client(self):
        """Setup OpenAI client for API-based transcription."""
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package not found. Install with: pip install openai")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.openai_client = openai.OpenAI(api_key=api_key)
        logger.info("OpenAI Whisper API client initialized")

    def _setup_third_party_client(self):
        """Validate third-party Whisper API configuration."""
        if not self.api_base_url:
            self.api_base_url = os.getenv("WHISPER_API_BASE_URL", "https://api.whisper-api.com")
        if not self.api_key:
            self.api_key = os.getenv("WHISPER_API_KEY")
        if not self.api_endpoint:
            self.api_endpoint = os.getenv("WHISPER_API_ENDPOINT", "/v1/transcriptions")
        if not self.api_key:
            raise ValueError("Missing WHISPER_API_KEY for third-party provider")
        logger.info(f"Third-party Whisper API configured: {self.api_base_url}{self.api_endpoint}")
    
    def _setup_local_model(self):
        """Setup local Whisper model."""
        if not WHISPER_AVAILABLE:
            raise ImportError(
                "whisper package not found. Install with: pip install openai-whisper"
            )
        
        try:
            logger.info(f"Loading Whisper model: {self.model_name}")
            self.model = whisper.load_model(self.model_name)
            logger.info(f"Whisper model '{self.model_name}' loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise

    def _ensure_local_model_loaded(self):
        """Ensure local model is loaded (lazy initialization)."""
        if self.model is None:
            self._setup_local_model()
    
    def transcribe_audio(
        self, 
        audio_path: str, 
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'es', 'fr')
            prompt: Optional prompt to guide transcription
            
        Returns:
            Dictionary containing transcription results
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Validate audio file
        if not validate_audio_file(str(audio_path)):
            raise ValueError(f"Invalid audio file: {audio_path}")
        
        logger.info(f"Starting transcription of: {audio_path.name}")
        
        try:
            if self.provider == "openai":
                return self._transcribe_with_api(audio_path, language, prompt)
            elif self.provider == "local":
                return self._transcribe_with_local_model(audio_path, language, prompt)
            elif self.provider == "whisper_api":
                return self._transcribe_with_third_party_api(audio_path, language, prompt)
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    def _transcribe_with_api(
        self, 
        audio_path: Path, 
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribe using OpenAI API."""
        with open(audio_path, "rb") as audio_file:
            transcript = self.openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
                prompt=prompt,
                response_format="verbose_json",
                timestamp_granularities=["segment"]
            )
        
        return {
            "text": transcript.text,
            "language": transcript.language,
            "duration": transcript.duration,
            "segments": transcript.segments,
            "method": "openai_api"
        }
    
    def _transcribe_with_local_model(
        self, 
        audio_path: Path, 
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribe using local Whisper model."""
        # Lazy-load model on first use
        self._ensure_local_model_loaded()
        options = {
            "verbose": False,
            "task": "transcribe"
        }
        
        if language:
            options["language"] = language
        if prompt:
            options["initial_prompt"] = prompt
        
        result = self.model.transcribe(str(audio_path), **options)
        
        return {
            "text": result["text"],
            "language": result["language"],
            "segments": result.get("segments", []),
            "method": "local_model",
            "model": self.model_name
        }

    def _transcribe_with_third_party_api(
        self,
        audio_path: Path,
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribe using a third-party Whisper-compatible API."""
        url = f"{self.api_base_url.rstrip('/')}/{self.api_endpoint.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {}
        if language:
            data["language"] = language
        if prompt:
            data["prompt"] = prompt
        files = {"file": (audio_path.name, open(audio_path, "rb"))}
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(url, headers=headers, data=data, files=files)
                resp.raise_for_status()
                payload = resp.json()
        finally:
            files["file"][1].close()

        # Normalization: Expect a common shape; adjust as needed for the provider
        text = payload.get("text") or payload.get("transcript") or payload.get("result")
        segments = payload.get("segments") or []
        lang = payload.get("language") or language
        return {
            "text": text or "",
            "language": lang,
            "segments": segments,
            "method": "third_party_api",
            "provider": "whisper_api",
        }
    
    def get_available_models(self) -> list:
        """Get list of available Whisper models."""
        if self.provider == "openai":
            return ["whisper-1"]
        if self.provider == "local":
            return ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
        if self.provider == "whisper_api":
            return ["remote-default"]
        return []


def create_whisper_service(config: Optional[Dict[str, Any]] = None) -> WhisperService:
    """
    Factory function to create WhisperService instance.
    
    Args:
        config: Configuration dictionary with keys:
            - model_name: str
            - use_openai_api: bool
            
    Returns:
        Configured WhisperService instance
    """
    if config is None:
        config = {}
    
    model_name = config.get("model_name", "base")
    use_openai_api = config.get("use_openai_api", False)
    provider = config.get("provider")
    api_base_url = config.get("api_base_url")
    api_key = config.get("api_key")
    api_endpoint = config.get("api_endpoint")

    return WhisperService(
        model_name=model_name,
        use_openai_api=use_openai_api,
        provider=provider,
        api_base_url=api_base_url,
        api_key=api_key,
        api_endpoint=api_endpoint,
    )