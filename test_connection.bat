@echo off
echo ================================================
echo Hospital System Connection Test
echo ================================================
echo.

set /p TARGET_IP="Enter the IP address to test (e.g., 192.168.43.247): "
set /p TARGET_PORT="Enter the port to test (e.g., 5001): "

echo.
echo Testing connection to %TARGET_IP%:%TARGET_PORT%
echo ================================================
echo.

echo Step 1: Ping Test
echo ------------------
ping -n 4 %TARGET_IP%
echo.

echo Step 2: Port Test (using curl)
echo -------------------------------
curl -m 5 http://%TARGET_IP%:%TARGET_PORT%/health
echo.

echo Step 3: Telnet Test (if available)
echo -----------------------------------
echo If telnet is installed, testing port...
telnet %TARGET_IP% %TARGET_PORT%
echo.

echo ================================================
echo Test Complete
echo ================================================
pause
