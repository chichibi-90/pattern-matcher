@echo off
echo ========================================
echo Starting Currency Pair Price Data Viewer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run setup.bat first or install Python
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Flask is not installed
    echo Please run setup.bat first to install dependencies
    pause
    exit /b 1
)

echo Starting Flask application...
echo.
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause


