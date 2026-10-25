const child_process = require('child_process');
function directForms(program, args, options) {
  child_process.exec(program);
  child_process.execSync(program);
  child_process.execFile(program, args);
  child_process.execFileSync(program, args);
  child_process.spawn(program, args);
  child_process.spawnSync(program, args);
  child_process.fork(program, args);
  child_process['exec'](program);
  tools.child_process.execFile(program, args);
  tools['child_process']['spawn'](program, args);
}
