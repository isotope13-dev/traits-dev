const os = require('node:os');
const path = require('node:path');
const file = path.join(os.homedir() || os.tmpdir(), '.app');
