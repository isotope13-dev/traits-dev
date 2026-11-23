const net = require('net');
const fs = require('fs');
const socket = new net.Socket();
socket.connect(9000, '127.0.0.1');
socket.on('data', chunk => {
  if (chunk.toString().startsWith('FILE_START:')) {
    const output = fs.createWriteStream('received.bin');
    output.write(chunk);
  }
});
