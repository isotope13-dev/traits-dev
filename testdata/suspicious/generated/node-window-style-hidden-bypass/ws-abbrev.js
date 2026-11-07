const { execFile } = require('child_process');
execFile('C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe', ['-NoP', '-w', 'hidden', '-exec', 'bypass', '-File', target]);
