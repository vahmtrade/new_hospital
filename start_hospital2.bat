@echo off
echo Starting Hospital 2 Server...
start cmd /k python server.py "General Hospital" 5002 general_hospital.db

timeout /t 3

echo Starting Hospital 2 GUI...
start cmd /k python gui.py "General Hospital" 5002

echo Hospital 2 started!
pause
