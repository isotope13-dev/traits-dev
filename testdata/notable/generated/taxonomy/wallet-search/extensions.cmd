@echo off
for %%f in (*.bat) do echo %%f
for /r "." %%f in (*.exe) do echo %%f
