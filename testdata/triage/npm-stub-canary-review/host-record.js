const os = require('os');
const host = os.hostname();
const encoded = Buffer.from(JSON.stringify({host})).toString('base64');
console.log(encoded);
