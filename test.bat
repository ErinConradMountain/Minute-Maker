@echo off
REM Quick test execution script for Windows

echo 🧪 Running Minute Maker Tests...

REM Run unit tests
echo Running unit tests...
python scripts\test_runner.py --type unit --verbose
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Unit tests failed!
    exit /b 1
)

REM Run integration tests
echo Running integration tests...
python scripts\test_runner.py --type integration --verbose
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Integration tests failed!
    exit /b 1
)

REM Generate coverage report
echo Generating coverage report...
python scripts\test_runner.py --type all --coverage

echo ✅ All tests completed!