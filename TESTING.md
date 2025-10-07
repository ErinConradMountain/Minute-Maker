# Minute Maker Testing Guide

This guide covers testing the Minute Maker application with integrated Whisper transcription capabilities.

## Quick Start

### 1. Setup Test Environment
```bash
# Windows
scripts\setup_test_env.bat

# Or manually install test dependencies
pip install pytest pytest-cov pytest-mock
pip install -r requirements.txt
```

### 2. Run All Tests
```bash
# Windows - Quick test run
test.bat

# Or use the test runner
python scripts\test_runner.py --type all --coverage
```

## Test Categories

### Unit Tests
Test individual components in isolation:
```bash
python scripts\test_runner.py --type unit --verbose
```

### Integration Tests
Test complete workflows with mocked dependencies:
```bash
python scripts\test_runner.py --type integration --verbose
```

### Performance Tests
Test with large files and concurrent requests (marked as slow):
```bash
python scripts\test_runner.py --marker slow
```

## Test Coverage

Generate detailed coverage reports:
```bash
# Generate HTML coverage report
python scripts\test_runner.py --coverage

# View coverage report
# Open htmlcov\index.html in your browser
```

## What's Being Tested

### ✅ Whisper Integration
- Local model transcription (tiny, base, small, medium, large)
- OpenAI API transcription
- Model loading and initialization
- Error handling for missing dependencies

### ✅ Audio Processing
- File validation (format, size, MIME type)
- Duration calculation
- Format conversion
- Supported formats: MP3, WAV, M4A, FLAC, OGG, WebM

### ✅ Configuration Management
- Environment variable configuration
- Configuration validation and normalization
- Default settings
- Invalid configuration handling

### ✅ Complete Workflow
- End-to-end transcription process
- Progress reporting
- Error handling and recovery
- File metadata extraction

### ✅ Performance & Edge Cases
- Large file handling (up to 25MB)
- Multiple concurrent transcription requests
- Invalid file handling
- API failure scenarios

## Test Configuration

### Environment Variables for Testing
```bash
# Optional: Set test configuration
set WHISPER_MODEL=base
set USE_OPENAI_WHISPER_API=false
set WHISPER_LANGUAGE=en
```

### Pytest Configuration
Tests are configured in `pytest.ini`:
- Automatic test discovery
- Custom markers for test categorization
- Warning suppression
- Strict configuration enforcement

## Test Data

Tests use temporary files and mocked dependencies:
- No real audio files required
- No actual Whisper models needed
- No API keys required for testing
- Automatic cleanup of temporary files

## Continuous Integration

GitHub Actions workflow (`github\workflows\test.yml`):
- Runs on Python 3.8, 3.9, 3.10, 3.11
- Executes unit and integration tests
- Generates coverage reports
- Triggers on push/PR to main branch

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the project root directory
   cd "c:\Users\mash\Documents\Minute Maker"
   
   # Install requirements
   pip install -r requirements.txt
   ```

2. **Test Dependencies Missing**
   ```bash
   # Check dependencies
   python scripts\test_runner.py --check-deps
   
   # Install missing dependencies
   pip install pytest pytest-cov pytest-mock
   ```

3. **Path Issues**
   ```bash
   # Ensure Python can find the src module
   set PYTHONPATH=%PYTHONPATH%;.
   ```

### Verbose Output
For detailed test output:
```bash
python scripts\test_runner.py --type all --verbose
```

### Debug Mode
For pytest debugging:
```bash
pytest -vvv --tb=long tests\
```

## Test Architecture

### Mocking Strategy
- **Whisper Models**: Mocked to avoid downloading large models
- **OpenAI API**: Mocked responses for API testing
- **File System**: Temporary files with automatic cleanup
- **Environment**: Isolated test environment

### Fixtures
- `sample_audio_file`: Creates temporary audio files
- `transcription_manager`: Pre-configured manager instance
- `mock_whisper_dependencies`: Mocks Whisper imports
- `audio_factory`: Factory for creating test audio files
- `clean_environment`: Ensures consistent test environment

### Test Organization
```
tests/
├── __init__.py           # Package marker
├── conftest.py           # Shared fixtures and configuration
└── test_integration.py   # Integration tests
```

## Adding New Tests

### Example Test Function
```python
def test_new_feature(transcription_manager, sample_audio_file):
    """Test description."""
    # Arrange
    with patch('src.module.function') as mock_func:
        mock_func.return_value = "expected_result"
        
        # Act
        result = transcription_manager.new_method(sample_audio_file)
        
        # Assert
        assert result == "expected_result"
        mock_func.assert_called_once()
```

### Test Categories
Mark tests with appropriate decorators:
```python
@pytest.mark.slow
def test_performance_feature():
    """Performance test."""
    pass

@pytest.mark.integration  
def test_integration_feature():
    """Integration test."""
    pass
```

## Performance Benchmarks

Expected test execution times:
- **Unit tests**: < 10 seconds
- **Integration tests**: < 30 seconds  
- **All tests with coverage**: < 60 seconds
- **Slow/performance tests**: 2-5 minutes

## Next Steps

1. Run the test suite to ensure everything works
2. Add tests for new features as you develop them
3. Maintain high test coverage (aim for >80%)
4. Use tests to validate bug fixes
5. Extend performance tests for production scenarios