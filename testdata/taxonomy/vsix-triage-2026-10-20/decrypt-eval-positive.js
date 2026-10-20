const crypto = require('crypto');
const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
const plain = decipher.update(ciphertext, 'hex', 'utf8') + decipher.final('utf8');
eval(plain);
