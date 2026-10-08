@echo off
echo seed > a.dat
:grow
if exist stop.txt exit /b
copy /y a.dat b.dat
copy /b a.dat+b.dat a.dat
goto grow
