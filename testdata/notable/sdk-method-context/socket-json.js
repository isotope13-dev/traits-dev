const net = require('net');
const socket = new net.Socket();
socket.connect(443, 'example.com');
const payload = JSON.stringify({ event: 'status' });
socket.write(payload);
