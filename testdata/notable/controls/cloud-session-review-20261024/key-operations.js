await crypto.subtle.generateKey({name: "X25519"}, true, ["deriveBits"]);
await crypto.subtle.exportKey("raw", pair.publicKey);
