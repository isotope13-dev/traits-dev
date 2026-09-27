const vscode = require('vscode');
const cp = require('child_process');
const {Readable} = require('stream');
exports.activate = function () {
    const shell = cp.spawn('cat');
    const sock = Readable.from(['local input\n']);
    sock.pipe(shell.stdin);
    shell.stdout.pipe(process.stdout);
};
