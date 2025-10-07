"""
Integration tests for the complete Minute Maker application with Whisper.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.core.transcription_manager import TranscriptionManager
from src.audio.whisper_service import WhisperService


class TestMinuteMakerIntegration:
    """Integration tests for the complete application."""
    
    @pytest.fixture
    def sample_audio_file(self):
        """Create a temporary audio file for testing."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            # Write some fake audio data
            f.write(b"fake mp3 audio data for testing")
            f.flush()
            yield f.name
        
        # Cleanup
        os.unlink(f.name)
    
    @pytest.fixture
    def transcription_manager(self):
        """Create TranscriptionManager instance with test configuration."""
        config = {
            "whisper": {
                "model_name": "base",
                "use_openai_api": False
            }
        }
        return TranscriptionManager(config)
    
    @patch('src.utils.audio_utils.validate_audio_file')
    @patch('src.audio.whisper_service.whisper')
    def test_complete_transcription_workflow(
        self, 
        mock_whisper, 
        mock_validate, 
        transcription_manager, 
        sample_audio_file
    ):
        """Test complete workflow from audio file to transcription."""
        # Setup mocks
        mock_validate.return_value = True
        mock_model = Mock()
        mock_model.transcribe.return_value = {
            "text": "Hello, this is a test meeting transcript.",
            "language": "en",
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "text": "Hello, this is a test meeting transcript."
                }
            ]
        }
        mock_whisper.load_model.return_value = mock_model
        
        # Track progress calls
        progress_calls = []
        
        def progress_callback(status, progress):
            progress_calls.append((status, progress))
        
        # Execute transcription
        result = transcription_manager.transcribe_file(
            sample_audio_file,
            progress_callback=progress_callback
        )
        
        # Verify results
        assert result["text"] == "Hello, this is a test meeting transcript."
        assert result["language"] == "en"
        assert result["method"] == "local_model"
        assert result["file_name"] == Path(sample_audio_file).name
        assert "file_size" in result
        
        # Verify progress was reported
        assert len(progress_calls) >= 3
        assert any("Validating" in call[0] for call in progress_calls)
        assert any("complete" in call[0].lower() for call in progress_calls)
    
    def test_get_transcription_info(self, transcription_manager):
        """Test getting transcription service information."""
        with patch('src.audio.whisper_service.whisper'):
            info = transcription_manager.get_service_info()
            
            assert "available_models" in info
            assert "current_model" in info
            assert "using_api" in info
            assert "supported_formats" in info
            
            assert info["current_model"] == "base"
            assert not info["using_api"]
            assert ".mp3" in info["supported_formats"]


class TestWhisperServiceIntegration:
    """Integration tests for WhisperService with different configurations."""
    
    @pytest.fixture
    def mock_whisper_result(self):
        """Mock Whisper transcription result."""
        return {
            "text": "This is a sample transcription from Whisper.",
            "language": "en",
            "segments": [
                {
                    "id": 0,
                    "seek": 0,
                    "start": 0.0,
                    "end": 3.0,
                    "text": "This is a sample transcription",
                    "tokens": [1, 2, 3, 4, 5],
                    "temperature": 0.0,
                    "avg_logprob": -0.5,
                    "compression_ratio": 1.2,
                    "no_speech_prob": 0.1
                },
                {
                    "id": 1,
                    "seek": 300,
                    "start": 3.0,
                    "end": 5.0,
                    "text": " from Whisper.",
                    "tokens": [6, 7, 8],
                    "temperature": 0.0,
                    "avg_logprob": -0.3,
                    "compression_ratio": 1.1,
                    "no_speech_prob": 0.05
                }
            ]
        }
    
    @patch('src.utils.audio_utils.validate_audio_file')
    @patch('src.audio.whisper_service.whisper')
    def test_local_model_transcription(
        self, 
        mock_whisper, 
        mock_validate, 
        mock_whisper_result
    ):
        """Test transcription with local Whisper model."""
        mock_validate.return_value = True
        mock_model = Mock()
        mock_model.transcribe.return_value = mock_whisper_result
        mock_whisper.load_model.return_value = mock_model
        
        with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
            temp_file.write(b"fake audio data")
            temp_file.flush()
            
            service = WhisperService(model_name="base", use_openai_api=False)
            result = service.transcribe_audio(temp_file.name)
            
            assert result["text"] == mock_whisper_result["text"]
            assert result["method"] == "local_model"
            assert result["model"] == "base"
            mock_model.transcribe.assert_called_once()
    
    @patch('src.utils.audio_utils.validate_audio_file')
    @patch('src.audio.whisper_service.openai')
    def test_openai_api_transcription(self, mock_openai, mock_validate):
        """Test transcription with OpenAI API."""
        mock_validate.return_value = True
        
        # Mock OpenAI client and response
        mock_client = Mock()
        mock_transcript = Mock()
        mock_transcript.text = "API transcription result"
        mock_transcript.language = "en"
        mock_transcript.duration = 10.5
        mock_transcript.segments = []
        
        mock_client.audio.transcriptions.create.return_value = mock_transcript
        mock_openai.OpenAI.return_value = mock_client
        
        # On Windows, close the temp file before re-opening in code under test
        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        try:
            temp.write(b"fake wav data")
            temp.flush()
            path = temp.name
        finally:
            temp.close()

        try:
            with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
                service = WhisperService(use_openai_api=True)
                result = service.transcribe_audio(path, language="en")
                
                assert result["text"] == "API transcription result"
                assert result["method"] == "openai_api"
                assert result["language"] == "en"
                mock_client.audio.transcriptions.create.assert_called_once()
        finally:
            os.unlink(path)

    @patch('src.utils.audio_utils.validate_audio_file')
    @patch('src.audio.whisper_service.httpx.Client')
    def test_third_party_whisper_api_transcription(self, mock_httpx_client, mock_validate):
        """Test transcription with third-party Whisper-compatible API (whisper_api)."""
        mock_validate.return_value = True

        # Mock HTTP client and response
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "text": "Third-party API transcription",
            "language": "en",
            "segments": [{"start": 0.0, "end": 1.0, "text": "Third-party API transcription"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_client_instance.post.return_value = mock_response
        mock_httpx_client.return_value.__enter__.return_value = mock_client_instance

        temp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        try:
            temp.write(b"fake data")
            temp.flush()
            path = temp.name
        finally:
            temp.close()

        try:
            service = WhisperService(
                provider="whisper_api",
                api_base_url="https://api.whisper-api.com",
                api_key="test-key",
                api_endpoint="/v1/transcriptions",
            )
            result = service.transcribe_audio(path, language="en")

            assert result["text"] == "Third-party API transcription"
            assert result["method"] == "third_party_api"
            assert result["provider"] == "whisper_api"
            mock_client_instance.post.assert_called_once()
        finally:
            os.unlink(path)


class TestAudioUtilsIntegration:
    """Integration tests for audio utilities."""
    
    def test_file_validation_workflow(self):
        """Test complete file validation workflow."""
        from src.utils.audio_utils import validate_audio_file, get_supported_formats
        
        # Test with various file types
        supported_formats = get_supported_formats()
        
        for ext in supported_formats:
            with tempfile.NamedTemporaryFile(suffix=ext) as temp_file:
                # Write small amount of data
                temp_file.write(b"fake audio data")
                temp_file.flush()
                
                # Should pass validation (mocked MIME type check)
                with patch('mimetypes.guess_type') as mock_mime:
                    mock_mime.return_value = (f'audio/{ext[1:]}', None)
                    assert validate_audio_file(temp_file.name)
    
    @patch('src.utils.audio_utils.PYDUB_AVAILABLE', True)
    @patch('src.utils.audio_utils.AudioSegment')
    def test_audio_processing_workflow(self, mock_audiosegment):
        """Test audio processing utilities."""
        from src.utils.audio_utils import get_audio_duration, convert_audio_format
        
        # Mock AudioSegment
        mock_audio = Mock()
        mock_audio.__len__ = Mock(return_value=45000)  # 45 seconds
        mock_audiosegment.from_file.return_value = mock_audio
        
        with tempfile.NamedTemporaryFile(suffix=".mp3") as input_file:
            with tempfile.NamedTemporaryFile(suffix=".wav") as output_file:
                # Test duration calculation
                duration = get_audio_duration(input_file.name)
                assert duration == 45.0
                
                # Test format conversion
                success = convert_audio_format(
                    input_file.name, 
                    output_file.name, 
                    "wav"
                )
                assert success
                mock_audio.export.assert_called_once_with(
                    output_file.name, 
                    format="wav"
                )


class TestConfigurationIntegration:
    """Integration tests for configuration management."""
    
    def test_whisper_config_validation(self):
        """Test Whisper configuration validation and defaults."""
        from src.config.whisper_config import (
            get_default_whisper_config, 
            validate_whisper_config
        )
        
        # Test default configuration
        default_config = get_default_whisper_config()
        assert default_config["model_name"] == "base"
        assert not default_config["use_openai_api"]
        
        # Test configuration validation
        invalid_config = {
            "model_name": "invalid_model",
            "temperature": 2.0,  # Invalid range
            "best_of": -1,  # Invalid value
        }
        
        validated = validate_whisper_config(invalid_config)
        assert validated["model_name"] == "base"  # Corrected
        assert validated["temperature"] == 0  # Corrected
        assert validated["best_of"] == 5  # Corrected
    
    def test_environment_variable_integration(self):
        """Test configuration from environment variables."""
        from src.config.whisper_config import get_default_whisper_config
        
        env_vars = {
            'WHISPER_MODEL': 'large',
            'USE_OPENAI_WHISPER_API': 'true',
            'WHISPER_LANGUAGE': 'es',
            'WHISPER_TEMPERATURE': '0.2'
        }
        
        with patch.dict('os.environ', env_vars):
            config = get_default_whisper_config()
            
            assert config["model_name"] == "large"
            assert config["use_openai_api"] is True
            assert config["language"] == "es"
            assert config["temperature"] == 0.2


@pytest.mark.slow
class TestPerformanceIntegration:
    """Performance and stress tests (marked as slow)."""
    
    @patch('src.audio.whisper_service.whisper')
    @patch('src.utils.audio_utils.validate_audio_file')
    def test_large_file_handling(self, mock_validate, mock_whisper):
        """Test handling of large audio files."""
        mock_validate.return_value = True
        mock_model = Mock()
        mock_model.transcribe.return_value = {
            "text": "Large file transcription",
            "language": "en",
            "segments": []
        }
        mock_whisper.load_model.return_value = mock_model
        
        # Create a larger temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
            # Write 1MB of fake data
            temp_file.write(b"x" * (1024 * 1024))
            temp_file.flush()
            
            service = WhisperService()
            
            # Should handle large file without issues
            result = service.transcribe_audio(temp_file.name)
            assert result["text"] == "Large file transcription"
    
    def test_multiple_transcription_requests(self):
        """Test handling multiple concurrent transcription requests."""
        from src.core.transcription_manager import TranscriptionManager
        
        with patch('src.audio.whisper_service.whisper') as mock_whisper:
            with patch('src.utils.audio_utils.validate_audio_file') as mock_validate:
                mock_validate.return_value = True
                mock_model = Mock()
                mock_model.transcribe.return_value = {
                    "text": "Concurrent transcription",
                    "language": "en",
                    "segments": []
                }
                mock_whisper.load_model.return_value = mock_model
                
                manager = TranscriptionManager()
                
                # Process multiple files
                results = []
                for i in range(3):
                    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
                        temp_file.write(f"file {i} data".encode())
                        temp_file.flush()
                        
                        result = manager.transcribe_file(temp_file.name)
                        results.append(result)
                
                # All should succeed
                assert len(results) == 3
                assert all(r["text"] == "Concurrent transcription" for r in results)