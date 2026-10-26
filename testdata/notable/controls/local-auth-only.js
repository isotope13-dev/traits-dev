const cp = require('child_process');
function check(password) {
  cp.execFileSync('/usr/bin/dscl', ['/Local/Default', '-authonly', process.env.USER, password]);
  return Buffer.from(password).toString('base64');
}
