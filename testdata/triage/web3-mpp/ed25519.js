async function sign(key, message) { return crypto.subtle.sign("Ed25519", key, message); }
