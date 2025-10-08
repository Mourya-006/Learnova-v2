@echo off
echo ========================================
echo   GitHub Security Verification
echo ========================================
echo.

echo Checking if .env is protected from Git...
echo.

git check-ignore .env >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ SAFE: .env is in .gitignore
) else (
    echo ❌ WARNING: .env is NOT ignored!
    echo    Fix: Make sure .gitignore includes .env
)

echo.
echo Checking what will be committed...
echo.

git ls-files | findstr ".env" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ❌ DANGER: .env is tracked by Git!
    echo    Fix: Run 'git rm --cached .env'
) else (
    echo ✅ SAFE: .env is not tracked by Git
)

echo.
echo Checking current git status...
echo.

git status --short | findstr ".env" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  WARNING: .env appears in git status
    echo    Do NOT commit this file!
) else (
    echo ✅ SAFE: .env not in pending changes
)

echo.
echo ========================================
if exist .env (
    echo ✅ .env file exists locally
) else (
    echo ⚠️  .env file not found
    echo    Create it using: setup_api_key.bat
)

if exist .env.example (
    echo ✅ .env.example exists for sharing
) else (
    echo ⚠️  .env.example not found
)

if exist .gitignore (
    findstr /C:".env" .gitignore >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ .gitignore contains .env
    ) else (
        echo ❌ .gitignore missing .env entry!
    )
) else (
    echo ❌ .gitignore file not found!
)

echo ========================================
echo.
echo Summary:
echo - Only commit .env.example (template)
echo - Never commit .env (actual key)
echo - Each person gets their own API key
echo.
echo Read SECURITY.md for more details
echo.
pause
