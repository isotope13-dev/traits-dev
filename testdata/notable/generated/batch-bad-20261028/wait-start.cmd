@echo off
:retry
start /wait tool.exe
goto retry
