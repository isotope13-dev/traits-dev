const tls = require('tls');
const node_https_9 = require('https');
const ctx = tls.createSecureContext({key, cert});
node_https_9.createServer({SNICallback: (name, cb) => cb(null, ctx)}, app);
