@echo off
echo seed > a.dat
:grow
copy /y a.dat b.dat
copy /b a.dat+b.dat a.dat
goto done
:done
echo finished
