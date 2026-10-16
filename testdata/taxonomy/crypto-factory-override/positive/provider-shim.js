// Provider shim: exports the Node cipher factory surface for consumers.
// The decipher calls below implement decryption as a service; no payload
// of its own is decrypted, and the globalThis calls are host bridges.
const nc = require('node:crypto');
exports.createHash = function (algorithm) { return nc.createHash(algorithm); };
exports.createDecipheriv = function (algo, key, iv) { return nc.createDecipheriv(algo, key, iv); };
function decryptWithHost(algo, key, iv, data) {
  const d = nc.createDecipheriv(algo, key, iv);
  return globalThis['__host_crypto_decrypt'](d, data);
}
module.exports.decryptWithHost = decryptWithHost;
