const cp = require('child_process');
const {Readable, Writable} = require('stream');
const child = cp.spawn('cat');
const input = Readable.from(['local input\n']);
const output = new Writable({write(chunk, enc, cb) { cb(); }});
input.pipe(child.stdin);
child.stdout.pipe(output);
