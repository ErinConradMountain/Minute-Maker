"""
Pytest configuration and shared fixtures.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch


@pytest.fixture(scope="session")
def test_data_dir():
    """Create temporary directory for test data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return {
        "whisper": {
            "model_name": "base",
            "use_openai_api": False,
            "language": None,
            "temperature": 0.0
        },
        "output": {
            "format": "docx",
            "template": "standard"
        }
    }


@pytest.fixture(autouse=True)
def clean_environment():
    """Clean environment variables for consistent testing."""
    env_vars_to_clean = [
        'OPENAI_API_KEY',
        'WHISPER_MODEL',
        'USE_OPENAI_WHISPER_API',
        'WHISPER_LANGUAGE'
    ]
    
    original_values = {}
    for var in env_vars_to_clean:
        original_values[var] = os.environ.get(var)
        if var in os.environ:
            del os.environ[var]
    
    yield
    
    # Restore original values
    for var, value in original_values.items():
        if value is not None:
            os.environ[var] = value


@pytest.fixture
def mock_whisper_dependencies():
    """Mock Whisper dependencies for testing."""
    with patch('src.audio.whisper_service.WHISPER_AVAILABLE', True):
        with patch('src.audio.whisper_service.whisper') as mock_whisper:
            with patch('src.utils.audio_utils.PYDUB_AVAILABLE', True):
                yield mock_whisper


class AudioFileFactory:
    """Factory for creating test audio files."""
    
    @staticmethod
    def create_mp3(content: bytes = b"fake mp3 data") -> str:
        """Create temporary MP3 file."""
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name
    
    @staticmethod
    def create_wav(content: bytes = b"fake wav data") -> str:
        """Create temporary WAV file."""
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name
    
    @staticmethod
    def cleanup(file_path: str):
        """Clean up temporary file."""
        if os.path.exists(file_path):
            os.unlink(file_path)


@pytest.fixture
def audio_factory():
    """Provide audio file factory for tests."""
    factory = AudioFileFactory()
    created_files = []
    
    # Override methods to track created files
    original_create_mp3 = factory.create_mp3
    original_create_wav = factory.create_wav
    
    def tracked_create_mp3(content=b"fake mp3 data"):
        file_path = original_create_mp3(content)
        created_files.append(file_path)
        return file_path
    
    def tracked_create_wav(content=b"fake wav data"):
        file_path = original_create_wav(content)
        created_files.append(file_path)
        return file_path
    
    factory.create_mp3 = tracked_create_mp3
    factory.create_wav = tracked_create_wav
    
    yield factory
    
    # Cleanup all created files
    for file_path in created_files:
        factory.cleanup(file_path)