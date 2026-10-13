@echo off
setlocal enabledelayedexpansion
title MockMate - Startup Manager

echo ============================================================
echo         MockMate - Interview Preparation Platform
echo ============================================================
echo.

:: 1. Navigate to script root directory
cd /d "%~dp0"

:: 2. Resolve Node.js and NPM
set "NODE_CMD="
where node >nul 2>nul
if %errorlevel% equ 0 (
    set "NODE_CMD=node"
) else (
    if exist "%USERPROFILE%\.nodejs\node-v20.18.0-win-x64\node.exe" (
        set "PATH=%USERPROFILE%\.nodejs\node-v20.18.0-win-x64;%PATH%"
        set "NODE_CMD=%USERPROFILE%\.nodejs\node-v20.18.0-win-x64\node.exe"
    ) else if exist "C:\Program Files\nodejs\node.exe" (
        set "PATH=C:\Program Files\nodejs;%PATH%"
        set "NODE_CMD=C:\Program Files\nodejs\node.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\node\node.exe" (
        set "PATH=%LOCALAPPDATA%\Programs\node;%PATH%"
        set "NODE_CMD=%LOCALAPPDATA%\Programs\node\node.exe"
    )
)

if not defined NODE_CMD (
    echo [ERROR] Node.js was not detected on your system.
    echo Please install Node.js 20+ from https://nodejs.org or ensure it is in PATH.
    pause
    exit /b 1
)

:: 3. Resolve Python interpreter
set "PYTHON_CMD="
if exist "%~dp0backend\.venv\Scripts\python.exe" (
    set "PYTHON_CMD=%~dp0backend\.venv\Scripts\python.exe"
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        echo [ERROR] Python environment was not found.
        echo Expected backend virtual environment at: backend\.venv\Scripts\python.exe
        pause
        exit /b 1
    )
)

echo [1/3] Checking running services...

:: Check if backend is already listening on port 8000
netstat -ano | findstr /R ":8000.*LISTENING" >nul 2>nul
if %errorlevel% equ 0 (
    echo  - Backend is already running on http://localhost:8000
) else (
    echo  - Starting FastAPI Backend on http://localhost:8000...
    start "MockMate Backend API (FastAPI)" cmd /k "cd /d ""%~dp0backend"" && ""%PYTHON_CMD%"" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
)

:: Check if frontend is already listening on port 3000
netstat -ano | findstr /R ":3000.*LISTENING" >nul 2>nul
if %errorlevel% equ 0 (
    echo  - Frontend is already running on http://localhost:3000
) else (
    echo  - Starting Next.js Frontend on http://localhost:3000...
    start "MockMate Frontend (Next.js)" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"
)

echo.
echo [2/3] Waiting for services to initialize...
timeout /t 3 /nobreak >nul 2>&1 || ping -n 4 127.0.0.1 >nul

echo.
echo [3/3] Opening web browser...
start http://localhost:3000

echo.
echo ============================================================
echo   MockMate is running!
echo ============================================================
echo   - Web Application:     http://localhost:3000
echo   - Backend API:         http://localhost:8000
echo   - API Documentation:   http://localhost:8000/api/docs
echo ============================================================
echo   To shut down services, run: stop_mockmate.bat
echo   or close the individual service terminal windows.
echo ============================================================
echo.
pause
