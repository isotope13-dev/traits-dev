@echo off
echo seed > a.dat
:grow
copy /y a.dat b.dat
copy /b a.dat+b.dat c.dat
goto grow
