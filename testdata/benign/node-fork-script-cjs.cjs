const cp = require('node:child_process');
const worker = cp.fork(__dirname + '/worker.js', [], { detached: true });
worker.unref();
