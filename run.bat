@echo off
echo ========================================
echo Farmer Resource Pooling System
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Run the application
echo Starting the application...
echo.
echo The application will be available at: http://localhost:3000
echo Press Ctrl+C to stop the server
echo.
python application.py

pause
