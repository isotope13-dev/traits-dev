@echo off
set TMP_DIR=%APP_HOME%\tmp
if exist "%TMP_DIR%" (
    cd "%TMP_DIR%"
    del *.* /s /q > nul
    cd ..
)
