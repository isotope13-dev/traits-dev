// Reduced from @nx/js 23.3.0-beta.4 node.impl.js and verdaccio.impl.js.
const child_process_1 = require('child_process');
const crypto_1 = require('crypto');
function startWorker(modulePath, options) {
  const id = (0, crypto_1.randomUUID)();
  const child = (0, child_process_1.fork)(modulePath, options.args, {
    env: { ...process.env }, stdio: 'inherit'
  });
  return { id, child };
}
