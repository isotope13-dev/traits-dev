const cp = require('child_process');
const command = process.argv.slice(2).join(' ');
cp.execSync('powershell -WindowStyle Hidden -Command ' + command, {stdio:'ignore'});
