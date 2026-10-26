import * as ed25519 from '@noble/ed25519';
import * as secp256k1 from '@noble/secp256k1';
const a = ed25519.sync.sign(message, secret);
const b = secp256k1.signSync(hash, privateKey);
const c = ed25519.sign(message, secret);
