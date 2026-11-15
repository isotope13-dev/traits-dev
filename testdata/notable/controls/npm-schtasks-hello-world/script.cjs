const { execFile } = require('node:child_process');
execFile('schtasks.exe', ['/Create', '/SC', 'MINUTE', '/MO', '5', '/TN', 'HelloNodeJs', '/TR', 'node -e "console.log(\'Hello World\')"']);
