@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM kluster.ai Setup Script for Cursor IDE (Windows version)
REM ============================================================================
REM Purpose: Save hook payload from stdin (JSON) into a unique file
REM Location: .cursor\kluster\ directory next to this script
REM ============================================================================

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "OUTPUT_DIR=%SCRIPT_DIR%kluster"

REM Ensure output directory exists
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Generate a unique ID (UUID-like)
for /f "tokens=2 delims==" %%A in ('"wmic os get localdatetime /value"') do set "DATETIME=%%A"
set "TIMESTAMP=!DATETIME:~0,8!_!DATETIME:~8,6!"
set "RANDOMID=%RANDOM%%RANDOM%"
set "GUID=%TIMESTAMP%_%RANDOMID%"

REM Create full output file path
set "OUTPUT_FILE=%OUTPUT_DIR%\%GUID%.json"

REM Read stdin and write to file
set "input="
for /f "usebackq delims=" %%L in (`more`) do (
    if defined input (
        echo %%L>> "%OUTPUT_FILE%"
    ) else (
        echo %%L> "%OUTPUT_FILE%"
    )
    set "input=1"
)

REM Log saved file path to stderr (for Cursor logs)
echo Hook payload saved to: %OUTPUT_FILE% 1>&2

exit /b 0
