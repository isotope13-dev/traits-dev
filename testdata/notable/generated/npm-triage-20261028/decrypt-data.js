const crypto = require('crypto');
const fs = require('fs');
const cp = require('child_process');
function decrypt(data, key, nonce) {
  const decipher = crypto.createDecipheriv('aes-256-gcm',key,nonce);
  return decipher.update(data);
}
function saveSettings(settings) { fs.writeFileSync('settings.json', JSON.stringify(settings)); }
function lint() { cp.execFile('python', ['-m','flake8']); }
