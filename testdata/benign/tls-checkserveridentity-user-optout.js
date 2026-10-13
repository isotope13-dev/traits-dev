// Driver-style TLS option forwarding: hostname verification stays on unless
// the caller explicitly opts out via checkServerIdentity: false (the
// documented Node opt-out). The empty callback is caller-gated plumbing,
// not a bypass.
const tls = require('tls');

function parseSslOptions(options) {
  const result = { host: options.host, rejectUnauthorized: true };
  if (options.checkServerIdentity === false) {
    result.checkServerIdentity = function() {
      return undefined;
    };
  } else if (typeof options.checkServerIdentity === 'function') {
    result.checkServerIdentity = options.checkServerIdentity;
  }
  return result;
}

function connect(options) {
  return tls.connect(parseSslOptions(options));
}

module.exports = { parseSslOptions, connect };
