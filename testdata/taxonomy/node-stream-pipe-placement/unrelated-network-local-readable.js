const net = require('net');
const {Readable} = require('stream');
const cp = require('child_process');
net.connect(8123, '127.0.0.1').end('health\n');
const shell = cp.spawn('cat');
const sock = Readable.from(['local input\n']);
sock.pipe(shell.stdin);
