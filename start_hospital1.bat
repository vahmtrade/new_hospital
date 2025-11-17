@echo off
echo Starting Hospital 1 Server...
start cmd /k python server.py "City Hospital" 5001 city_hospital.db

timeout /t 3

echo Starting Hospital 1 GUI...
start cmd /k python gui.py "City Hospital" 5001

echo Hospital 1 started!
pause
