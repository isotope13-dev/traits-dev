// Local diagnostics and unrelated status traffic; no result-to-send relation.
const cp = require('child_process'), net = require('net'), dns = require('dns');
const sock = net.connect(443, '93.184.216.34');
sock.write('health check');
cp.exec('ps aux', (error, stdout) => console.log(stdout));
const record = Buffer.from(JSON.stringify({status:'ok'})).toString('base64');
dns.resolve4('example.invalid', (error, addresses) => console.log(addresses, record));
