const envelope = {"encryptedKey": "key", "iv": "iv", "ciphertext": "data"};
const algorithm = "RSA-OAEP AES-256-GCM";
const publicKey = "-----BEGIN PUBLIC KEY-----";
console.log(envelope, algorithm, publicKey);
