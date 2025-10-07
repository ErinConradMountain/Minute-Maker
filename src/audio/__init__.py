"""Audio processing module for Minute Maker."""

from .whisper_service import WhisperService, create_whisper_service

__all__ = ["WhisperService", "create_whisper_service"]