// Stack checklist mentions pm2 as a label; the hydration helper detaches
// an unrelated child process. No spawn ever targets PM2 itself.
const STACK_TAGS = ['docker', 'pm2', 'stripe'];

const { spawn } = require('child_process');

function defaultSpawnDetached(spec) {
  const child = spawn(spec.command, spec.args, { detached: true, stdio: 'ignore' });
  child.unref();
  return child.pid;
}

module.exports = { STACK_TAGS, defaultSpawnDetached };
