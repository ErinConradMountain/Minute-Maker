"""
Audio file utilities for validation and format conversion.
"""

import os
import mimetypes
from pathlib import Path
from typing import List, Optional

# Provide placeholder so tests can patch even if import fails
AudioSegment = None  # type: ignore

try:
    from pydub import AudioSegment  # type: ignore  # noqa: F401
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


# Supported audio formats
SUPPORTED_AUDIO_FORMATS = {
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.m4a': 'audio/mp4',
    '.flac': 'audio/flac',
    '.ogg': 'audio/ogg',
    '.webm': 'audio/webm'
}

# Maximum file size (25MB)
MAX_FILE_SIZE = 25 * 1024 * 1024


def validate_audio_file(file_path: str) -> bool:
    """
    Validate audio file format and size.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        True if file is valid, False otherwise
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return False
    
    # Check file size
    if file_path.stat().st_size > MAX_FILE_SIZE:
        return False
    
    # Check file extension
    file_ext = file_path.suffix.lower()
    if file_ext not in SUPPORTED_AUDIO_FORMATS:
        return False
    
    # Verify MIME type
    mime_type, _ = mimetypes.guess_type(str(file_path))
    expected_mime = SUPPORTED_AUDIO_FORMATS[file_ext]
    
    if mime_type and not mime_type.startswith('audio/'):
        return False
    
    return True


def get_audio_duration(file_path: str) -> Optional[float]:
    """
    Get audio file duration in seconds.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Duration in seconds, or None if unable to determine
    """
    if not PYDUB_AVAILABLE:
        return None
    
    try:
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # Convert from milliseconds
    except Exception:
        return None


def convert_audio_format(
    input_path: str, 
    output_path: str, 
    target_format: str = "wav"
) -> bool:
    """
    Convert audio file to different format.
    
    Args:
        input_path: Source audio file path
        output_path: Destination file path
        target_format: Target format (wav, mp3, etc.)
        
    Returns:
        True if conversion successful, False otherwise
    """
    if not PYDUB_AVAILABLE:
        return False
    
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=target_format)
        return True
    except Exception:
        return False


def get_supported_formats() -> List[str]:
    """Get list of supported audio file extensions."""
    return list(SUPPORTED_AUDIO_FORMATS.keys())


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
