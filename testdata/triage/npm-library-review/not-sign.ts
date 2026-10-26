const a = ed25519.sync.verify(signature, message, publicKey);
const b = secp256k1.getPublicKey(privateKey);
