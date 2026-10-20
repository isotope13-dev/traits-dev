const crypto = require('crypto');
function decryptCredential(text, key, iv) {
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
  const plain = decipher.update(text, 'hex', 'utf8') + decipher.final('utf8');
  return JSON.parse(plain);
}
const moduleName = 'require';
eval(moduleName);
