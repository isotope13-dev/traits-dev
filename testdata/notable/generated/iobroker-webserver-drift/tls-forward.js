const https = require('https');
const tls = require('tls');
const ctx = tls.createSecureContext({key, cert});
https.createServer({SNICallback: (name, cb) => cb(null, ctx)}, (req, res) => {
 const upstream = https.request({hostname: req.headers.host, path: req.url});
 req.pipe(upstream);
 upstream.on('response', reply => reply.pipe(res));
});
