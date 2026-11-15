const fs = require('fs');
const script = '/tmp/generated-script.py';
fs.writeFileSync(script, Buffer.from(process.env.SCRIPT, 'base64').toString('utf8'), { mode: 0o755 });
