@echo off
echo ================================================
echo Basic Hospital System Test
echo ================================================
echo.
echo This will test if the system works on THIS computer
echo.
pause

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from python.org
    pause
    exit
)
echo Python is installed OK
echo.

echo Step 2: Checking required packages...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ERROR: Flask is not installed!
    echo Installing required packages...
    pip install flask requests pillow
    echo.
)
echo Packages OK
echo.

echo Step 3: Testing database creation...
python -c "from database import HospitalDatabase; db = HospitalDatabase('test.db', 'Test Hospital'); print('Database OK')"
if errorlevel 1 (
    echo ERROR: Database test failed!
    pause
    exit
)
echo.

echo Step 4: Starting test server on port 5001...
echo.
echo A new window will open with the server.
echo Leave it running and come back to this window.
echo.
pause

start cmd /k python server.py "Test Hospital" 5001 test_hospital.db

echo Waiting 5 seconds for server to start...
timeout /t 5

echo.
echo Step 5: Testing server connection...
python -c "import requests; r = requests.get('http://localhost:5001/health', timeout=5); print('Server Response:', r.json())"
if errorlevel 1 (
    echo ERROR: Cannot connect to server!
    echo Check the server window for errors.
    pause
    exit
)

echo.
echo ================================================
echo SUCCESS! Basic system is working!
echo ================================================
echo.
echo Now you can:
echo 1. Close the test server window
echo 2. Try running start_master.bat
echo.
pause
