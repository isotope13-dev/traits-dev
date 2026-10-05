const crypto = require('crypto');
const dgram = require('dgram');
const socket = dgram.createSocket('udp4');
const tid = crypto.randomBytes(12);
const request = Buffer.alloc(20);
request.writeUInt16BE(1, 0);
request.writeUInt32BE(0x2112a442, 4);
tid.copy(request, 8);
socket.on('message', packet => {
    if (packet.length < 20) return;
    if (packet.readUInt16BE(0) !== 0x0101 || packet.readUInt32BE(4) !== 0x2112a442) return;
    if (!packet.subarray(8, 20).equals(tid)) return;
    socket.close();
});
socket.send(request, 19302, 'stun.l.google.com');
