const aes = require('aes-js');
const cipher = new aes.ModeOfOperation.cbc(key, iv);
const encrypted = cipher.encrypt(data);
