@echo off
echo Setting up test environment for Minute Maker...

REM Install test dependencies
echo Installing test dependencies...
pip install pytest pytest-cov pytest-mock pytest-asyncio

REM Install application dependencies for testing
echo Installing application dependencies...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found, installing core dependencies...
    pip install openai python-docx httpx
)

REM Create test data directory
if not exist tests\data mkdir tests\data

REM Run dependency check
echo Checking test setup...
python scripts\test_runner.py --check-deps

if %ERRORLEVEL% EQU 0 (
    echo ✅ Test environment setup complete!
    echo.
    echo Run tests with:
    echo   python scripts\test_runner.py --type unit       # Unit tests only
    echo   python scripts\test_runner.py --type integration    # Integration tests
    echo   python scripts\test_runner.py --coverage       # With coverage report
    echo   pytest -q                                      # Quick run
) else (
    echo ❌ Test environment setup failed!
    exit /b 1
)