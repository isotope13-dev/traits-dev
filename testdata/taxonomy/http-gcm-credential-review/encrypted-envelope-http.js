// Authenticated encryption used by an ordinary HTTP client.
const crypto = require('crypto');
const https = require('https');
function uploadStatus(status, key) {
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
    const ciphertext = Buffer.concat([cipher.update(JSON.stringify(status)), cipher.final()]);
    const envelope = Buffer.concat([iv, ciphertext, cipher.getAuthTag()]);
    const req = https.request({hostname: 'example.invalid', method: 'POST'});
    req.write(envelope);
    req.end();
}
