@echo off
echo ================================================
echo Hospital Management System - Firewall Setup
echo ================================================
echo.
echo This will add firewall rules to allow ports 5000, 5001, 5002
echo.
echo NOTE: You must run this as Administrator!
echo.
pause

echo Adding firewall rules...
echo.

netsh advfirewall firewall add rule name="Hospital System Port 5000" dir=in action=allow protocol=TCP localport=5000
echo Port 5000 added.

netsh advfirewall firewall add rule name="Hospital System Port 5001" dir=in action=allow protocol=TCP localport=5001
echo Port 5001 added.

netsh advfirewall firewall add rule name="Hospital System Port 5002" dir=in action=allow protocol=TCP localport=5002
echo Port 5002 added.

echo.
echo ================================================
echo Firewall rules added successfully!
echo ================================================
echo.
echo You can now run the hospital system.
echo.
pause
