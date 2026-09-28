const envelope = {"encryptedKey": "key", "iv": "iv", "ciphertext": "data"};
const algorithm = "RSA-OAEP AES-256-GCM";
const publicKey = "-----BEGIN PUBLIC KEY-----";
fetch('https://example.invalid/receive', {method: 'POST', body: JSON.stringify(envelope)});
sendEnvelope(fetch, envelope);
