// Benign local config decryptor: AES-CBC unlocks a config file at
// startup. No network POST, no executable drop, no shell launch.
const crypto = require('crypto');
const fs = require('fs');

function loadConfig(path, keyHex) {
  const blob = fs.readFileSync(path);
  const decipher = crypto.createDecipheriv(
    'aes-256-cbc',
    Buffer.from(keyHex, 'hex'),
    Buffer.alloc(16, 0)
  );
  const plain = Buffer.concat([decipher.update(blob), decipher.final()]);
  return JSON.parse(plain.toString('utf8'));
}

module.exports = { loadConfig };
