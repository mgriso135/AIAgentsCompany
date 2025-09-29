@echo off
title CEO Agent Session

:: Prompt the user to enter the API key for this session
set /p API_KEY="Please enter the Gemini API Key for this session and press Enter: "

:: Check if a key was entered
if not defined API_KEY (
    echo No API Key entered. Aborting.
    pause
    exit /b
)

echo Launching CEO AI Agent...

:: Execute the PowerShell script, passing the API key as a parameter
@powershell.exe -ExecutionPolicy Bypass -File "%~dp0ceo.ps1" -ApiKey "%API_KEY%"

echo Agent session finished.
pause