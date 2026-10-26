// A local AES-GCM decryptor and an unrelated, plaintext HTTP upload.
const crypto = require('crypto');
const https = require('https');
function unlockToken(raw, key) {
    const dec = crypto.createDecipheriv('aes-256-gcm', key, raw.slice(0, 12));
    dec.setAuthTag(raw.slice(raw.length - 16));
    return Buffer.concat([dec.update(raw.slice(12, -16)), dec.final()]);
}
function uploadStatus(status) {
    const req = https.request({hostname: 'example.invalid', method: 'POST'});
    req.write(JSON.stringify(status));
    req.end();
}
