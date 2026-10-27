const crypto = require('node:crypto');
function recoverBackup(encoded, key, iv) {
  const raw = Buffer.from(encoded, 'base64');
  const decoder = crypto.createDecipheriv('aes-128-cbc', key, iv);
  return Buffer.concat([decoder.update(raw), decoder.final()]);
}
module.exports = recoverBackup;
