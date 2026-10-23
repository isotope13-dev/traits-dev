const tls = require('node:tls');
function connect(host) {
  return tls.connect({host, port: 443, rejectUnauthorized: true});
}
