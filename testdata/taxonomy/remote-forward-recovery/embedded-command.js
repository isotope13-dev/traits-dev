const { execFileSync } = require('node:child_process');
execFileSync('powershell.exe', ['-Command', 'Get-CimInstance Win32_Shadowcopy | Remove-CimInstance']);
