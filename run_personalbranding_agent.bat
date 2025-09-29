@echo off
title Personal Branding Agent Session

:: Prompt the user to enter the API key for this session
set /p API_KEY="Please enter the Gemini API Key for this session and press Enter: "

:: Check if a key was entered
if not defined API_KEY (
    set API_KEY=AIzaSyD0kk9H5-YBVlImYC8skKbW2rumrxabdtg
)

echo %API_KEY%
echo Launching Personal Branding AI Agent...

:: Execute the PowerShell script, passing the API key as a parameter
@powershell.exe -ExecutionPolicy Bypass -File "%~dp0agent_personalbranding.ps1" -ApiKey "%API_KEY%"

echo Agent session finished.
pause