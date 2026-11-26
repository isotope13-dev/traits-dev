@echo off
set "MEGA_DIR1=%LOCALAPPDATA%\MEGAcmd"
set "MEGA_DIR2=%ProgramFiles%\MEGAcmd"
set "PATH=%MEGA_DIR1%;%MEGA_DIR2%;%PATH%"

:: === הפרטים שלך ===
set "GDRIVE_FILE_ID=1-JifxlH-RCePlcg-146NPonAt3FZg3vo"
set "MEGA_EMAIL=your-email@example.com"
set "MEGA_PASS=your-password"

:: ניקוי קבצים זמניים קודמים
del "%TEMP%\MEGAcmdSetup64.exe" >nul 2>&1

:: 1. הורדה חכמה מ-Google Drive (עוקפת את דף האזהרה של סריקת וירוסים) והתקנה
if not exist "%MEGA_DIR1%\MEGAcmdShell.exe" if not exist "%MEGA_DIR2%\MEGAcmdShell.exe" (
    echo Downloading MEGA CMD from Google Drive...
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "$id = '%GDRIVE_FILE_ID%'; " ^
        "$out = \"$env:TEMP\MEGAcmdSetup64.exe\"; " ^
        "$url = \"https://google.com\"; " ^
        "$res = Invoke-WebRequest -Uri $url -SessionVariable s; " ^
        "if ($res.Content -match 'confirm=([0-9A-Za-z_\-]+)') { " ^
        "  $confirm = $matches[1]; " ^
        "  Invoke-WebRequest -Uri \"https://google.com\" -WebSession $s -OutFile $out; " ^
        "} else { " ^
        "  Invoke-WebRequest -Uri \"https://google.com\" -WebSession $s -OutFile $out; " ^
        "}"

    echo Installing MEGA CMD silently... Please wait...
    start /wait "" "%TEMP%\MEGAcmdSetup64.exe" /VERYSILENT /NORESTART
    del "%TEMP%\MEGAcmdSetup64.exe" >nul 2>&1
)

:: בדיקה שההתקנה הצליחה
if not exist "%MEGA_DIR1%\MEGAcmdShell.exe" if not exist "%MEGA_DIR2%\MEGAcmdShell.exe" (
    echo ERROR: Installation failed!
    pause
    exit /b
)

:: 2. התחברות לחשבון MEGA
echo Checking login status...
call mega-whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Logging into MEGA...
    call mega-login "%MEGA_EMAIL%" "%MEGA_PASS%"
)

:: 3. העלאת התיקיות ל-MEGA
echo Starting backup to MEGA...
call mega-put -c "%USERPROFILE%\Desktop" "/PC_Backup/Desktop"
call mega-put -c "%USERPROFILE%\Documents" "/PC_Backup/Documents"
call mega-put -c "%USERPROFILE%\Pictures" "/PC_Backup/Pictures"
call mega-put -c "%USERPROFILE%\Downloads" "/PC_Backup/Downloads"

echo Upload complete!
pause
