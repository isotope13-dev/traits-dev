const crypto = require('crypto');
module.exports = { encrypt, decrypt, createCipher, createSign, createVerify, scrypt, randomBytes, createDecipher };
exports.encrypt = encrypt;
exports.scrypt = scrypt;
exports.createCipher = crypto.createCipher;
exports.createHash = crypto.createHash;
exports.createSign = crypto.createSign;
