
const cp = require('child_process');
const run = (exe, args) => cp.execFile(exe, args, { windowsHide: true });
run(sevenZip, ['x', archive, '-o' + dest, '-p' + secret, '-y']);
