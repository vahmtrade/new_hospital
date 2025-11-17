@echo off
echo Starting Master Hospital Server...
start cmd /k python server.py "Central Hospital" 5000 central_hospital.db

timeout /t 3

echo Starting Master Hospital GUI...
start cmd /k python gui.py "Central Hospital" 5000 master

echo Master Hospital started!
echo.
echo To connect to other hospitals:
echo 1. Go to the "Master Control" tab
echo 2. Add hospital URLs like: http://localhost:5001 or http://192.168.1.100:5001
echo.
pause
