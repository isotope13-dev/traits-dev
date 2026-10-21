// Static scanner fixture. Never execute.
const {spawn} = require('child_process');
const vbs = 'Set sh = CreateObject("Shell.Application")\nsh.ShellExecute "setup.exe", "", "", "runas", 1';
spawn('wscript.exe', ['setup.vbs'], {detached: false, stdio: 'ignore'});
