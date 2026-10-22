const algorithm = 'aes-256-gcm';
const derived = crypto.scryptSync(password, salt, 32);
const salt = record[key](0x00,0x10);
const iv = record[key](0x10,0x20);
const tag = record[key](0x20,0x30);
require(decrypt(derived, iv, tag));
