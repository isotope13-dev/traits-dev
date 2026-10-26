const child_process = require('child_process');
child_process.exec('echo test');
child_process.execSync('echo test');
child_process.execFile('tool', ['arg']);
