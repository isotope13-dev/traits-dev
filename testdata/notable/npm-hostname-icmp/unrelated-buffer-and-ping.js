const os = require('os');
const {exec} = require('child_process');
console.log(Buffer.from(os.hostname()).toString('hex'));
exec(`ping -c 1 ${process.argv[2]}`);
