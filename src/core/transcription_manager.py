"""
Main transcription manager that orchestrates the transcription process.
"""

import logging
from typing import Dict, Any, Optional, Callable
from pathlib import Path

from ..audio.whisper_service import create_whisper_service, WhisperService
from ..utils.audio_utils import validate_audio_file, get_audio_duration


logger = logging.getLogger(__name__)


class TranscriptionManager:
    """Manages the audio transcription process."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize transcription manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.whisper_service = create_whisper_service(self.config.get("whisper", {}))
        
    def transcribe_file(
        self, 
        audio_path: str,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> Dict[str, Any]:
        """
        Transcribe audio file with progress reporting.
        
        Args:
            audio_path: Path to audio file
            progress_callback: Function to call with progress updates
            
        Returns:
            Transcription results
        """
        audio_path = Path(audio_path)
        
        if progress_callback:
            progress_callback("Validating audio file...", 0.1)
        
        # Validate file
        if not validate_audio_file(str(audio_path)):
            raise ValueError(f"Invalid audio file: {audio_path}")
        
        # Get file info
        duration = get_audio_duration(str(audio_path))
        file_size = audio_path.stat().st_size
        
        logger.info(f"Transcribing file: {audio_path.name}")
        logger.info(f"File size: {file_size / (1024*1024):.1f} MB")
        if duration:
            logger.info(f"Duration: {duration:.1f} seconds")
        
        if progress_callback:
            progress_callback("Starting transcription...", 0.2)
        
        # Perform transcription
        try:
            result = self.whisper_service.transcribe_audio(
                str(audio_path),
                language=self.config.get("language"),
                prompt=self.config.get("prompt")
            )
            
            if progress_callback:
                progress_callback("Transcription complete!", 1.0)
            
            # Add metadata
            result.update({
                "file_name": audio_path.name,
                "file_size": file_size,
                "duration": duration,
                "config": self.config
            })
            
            logger.info("Transcription completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            if progress_callback:
                progress_callback(f"Transcription failed: {str(e)}", -1)
            raise
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about the transcription service."""
        return {
            "available_models": self.whisper_service.get_available_models(),
            "current_model": self.whisper_service.model_name,
            "using_api": self.whisper_service.use_openai_api,
            "supported_formats": [".mp3", ".wav", ".m4a", ".flac", ".ogg", ".webm"]
        }