const forge = require('node-forge');
const pem = forge.util.decode64(encodedPublicKey);
const key = forge.pki.publicKeyFromPem(pem);
const wrapped = key.encrypt(aesKey, 'RSAES-PKCS1-V1_5');
const cipher = forge.cipher.createCipher('AES-GCM', aesKey);
const payload = forge.util.encode64(cipher.output.getBytes());
