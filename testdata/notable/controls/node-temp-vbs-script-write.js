const fs = require('fs');
const os = require('os');
const path = require('path');
const script = 'WScript.Echo "local helper"';
fs.writeFileSync(path.join(os.tmpdir(), 'local-helper.vbs'), script);
