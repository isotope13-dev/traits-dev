const os = require('node:os');
const path = require('node:path');
const config = path.join(os.homedir() || os.tmpdir(), '.service', 'config.json');
