@echo off
powershell -Command "Invoke-WebRequest https://example.test/data.json -OutFile settings.json"
del "%~f0"
