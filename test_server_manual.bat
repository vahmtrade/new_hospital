@echo off
echo Starting test server...
echo.
echo Watch for any errors below:
echo ========================================
echo.

python server.py "Test Hospital" 5001 test_hospital.db

echo.
echo ========================================
echo Server stopped or crashed!
echo.
pause
