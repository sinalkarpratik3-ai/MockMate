@echo off
title MockMate - Service Shutdown

echo ============================================================
echo         MockMate - Stopping Local Development Services
echo ============================================================
echo.

set "STOPPED_ANY=0"

:: Terminate process listening on port 8000 (Backend API)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /R ":8000.*LISTENING"') do (
    echo Stopping Backend process on port 8000 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>nul
    set "STOPPED_ANY=1"
)

:: Terminate process listening on port 3000 (Frontend Web)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /R ":3000.*LISTENING"') do (
    echo Stopping Frontend process on port 3000 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>nul
    set "STOPPED_ANY=1"
)

if "%STOPPED_ANY%"=="0" (
    echo No active MockMate services were found on ports 8000 or 3000.
) else (
    echo.
    echo All MockMate local services have been stopped successfully.
)

echo.
timeout /t 2 /nobreak >nul 2>&1 || ping -n 3 127.0.0.1 >nul
