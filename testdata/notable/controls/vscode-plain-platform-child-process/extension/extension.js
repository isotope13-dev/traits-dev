const child = require('child_process');
if (process.platform === 'win32') {
  setTimeout(() => child.execFile('tool.exe', ['--version']), 1500);
}
module.exports = { activate() {} };
