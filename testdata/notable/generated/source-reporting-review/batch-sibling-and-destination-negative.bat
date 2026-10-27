@echo off
copy "%~dp0payload.bin" "%~dp0output.bin"
copy source.bin "%~f0"
type "%~dp0"
copy "0" output.bin
