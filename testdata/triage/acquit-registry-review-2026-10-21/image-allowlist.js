// Static scanner fixture. Never execute.
const trusted = ['explorer.exe', 'rundll32.exe', 'FileProtocolHandler'];
const child = require('child_process').spawn('cscript.exe', ['job.vbs'], {detached: true, stdio: 'ignore'});
child.unref();
