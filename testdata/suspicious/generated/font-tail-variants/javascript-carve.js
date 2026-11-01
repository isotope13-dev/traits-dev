const fs = require('fs');
const data = fs.readFileSync('Display-Regular.woff').toString('utf8');
const payload = Buffer.from(data.split('%%BOUNDARY%%')[1], 'base64');
fs.writeFileSync('decoded.bin', payload);
