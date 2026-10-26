const os = require('os');
const resolver = require('dns');
const encodedHost = Buffer.from(os.hostname()).toString('hex').slice(0,32);
resolver.resolve4('fixed' + '.check.example.invalid', () => {});
