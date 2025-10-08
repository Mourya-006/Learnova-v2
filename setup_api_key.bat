@echo off
echo ========================================
echo   Learnova - Gemini API Setup
echo ========================================
echo.

set /p API_KEY="Enter your Gemini API key: "

if "%API_KEY%"=="" (
    echo Error: API key cannot be empty!
    pause
    exit /b 1
)

echo.
echo Creating .env file...
echo GEMINI_API_KEY=%API_KEY%> .env

echo.
echo ========================================
echo   Setup Complete! ✅
echo ========================================
echo.
echo Your API key has been saved to .env file
echo.
echo Next steps:
echo 1. Close this window
echo 2. Restart your Flask app: python app.py
echo 3. Look for this message:
echo    ✅ Gemini AI successfully initialized!
echo.
pause
