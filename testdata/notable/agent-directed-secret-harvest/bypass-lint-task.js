// Near miss: an unattended agent run with its approval prompts disabled, given
// an ordinary repair task. No secret-file search is requested.
const { spawnSync } = require('child_process');

const PROMPT = 'Fix the lint errors reported in src/index.js and rerun the test suite.';

spawnSync('claude', ['--dangerously-skip-permissions', '-p', PROMPT], {
  stdio: 'inherit',
});
