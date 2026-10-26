const net = require('net');
const {spawn} = require('child_process');
const {PassThrough} = require('stream');
net.connect(8123, '127.0.0.1').end('health\n');
const peer = new PassThrough();
const first = spawn('/bin/sh', ['-c', 'cat']);
const second = spawn('/bin/sh', ['-c', 'printf ready']);
peer.pipe(first.stdin);
second.stdout.pipe(peer);
