@echo off
rem list running service host instances for the asset report
tasklist /fi "imagename eq svchost.exe" /fo table
