const crypto = require('crypto');
function recover(prefix, action, signature) {
  for (let n = 0; n < 2147483647; n++) {
    const inner = crypto.createHash('md5').update(prefix).update(String(n));
    const candidate = inner.digest('hex');
    const observed = crypto.createHash('md5').update(action + candidate).digest('hex');
    if (observed === signature) return candidate;
  }
}
const prefix = Buffer.from(publicKey).toString('base64');
