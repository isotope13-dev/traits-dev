@echo off
rem hardware inventory line for the asset report
for /f "tokens=2 delims==" %%a in ('wmic computersystem get manufacturer /value') do echo %%a
