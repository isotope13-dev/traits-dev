const forge = require('node-forge');
const names = ['forge.util.decode64', 'forge.util.encode64'];
const cipher = forge.cipher.createDecipher('AES-GCM', aesKey);
