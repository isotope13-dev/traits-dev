use secp256k1::{Message, PublicKey, Secp256k1, SecretKey};

pub fn check_pair(key_bytes: &[u8], msg_bytes: &[u8]) -> bool {
    let secp = Secp256k1::new();
    let key = SecretKey::from_slice(key_bytes).unwrap();
    let msg = Message::from_slice(msg_bytes).unwrap();
    let sig = secp.sign_ecdsa(&msg, &key);
    let pubkey = PublicKey::from_secret_key(&secp, &key);
    secp.verify_ecdsa(&msg, &sig, &pubkey).is_ok()
}
