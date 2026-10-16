// Same primitives with no factory exports: a payload decrypting its own
// blob keeps the hostile verdict.
const nc = require('node:crypto');
function runPayload(key, iv, blob) {
  const d = nc.createDecipheriv('aes-256-gcm', key, iv);
  const text = d.update(blob, 'base64', 'utf8');
  return globalThis[text](1);
}
module.exports.runPayload = runPayload;
