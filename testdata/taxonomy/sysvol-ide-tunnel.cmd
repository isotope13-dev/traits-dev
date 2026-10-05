@echo off
copy \\controller\SYSVOL\corp.test\scripts\deploy\* C:\ProgramData\stage /y
code.exe tunnel service install --accept-server-license-terms
