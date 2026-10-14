use secp256k1::{Message, Secp256k1, SecretKey};

pub fn sign_recoverable(key_bytes: &[u8], msg_bytes: &[u8]) -> Vec<u8> {
    let secp = Secp256k1::new();
    let key = SecretKey::from_slice(key_bytes).unwrap();
    let msg = Message::from_slice(msg_bytes).unwrap();
    let (rec_id, data) = secp.sign_ecdsa_recoverable(&msg, &key).serialize_compact();
    let mut out = vec![rec_id.to_i32() as u8];
    out.extend_from_slice(&data);
    out
}
