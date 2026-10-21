const cp = require('child_process');
cp.spawn('echo', ['review'], {
  shell:!0,
  detached:true
});
