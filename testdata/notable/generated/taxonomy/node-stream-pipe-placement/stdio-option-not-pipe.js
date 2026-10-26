const cp = require('child_process');
const child = cp.spawn('cat', [], {stdio: ['ignore', 'inherit', 'inherit']});
void child;
