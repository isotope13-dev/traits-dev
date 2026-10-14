use ed25519_dalek::{Signature, Signer, SigningKey};
use rand::rngs::OsRng;

pub fn sign_ed(msg: &[u8]) -> Signature {
    let key = SigningKey::generate(&mut OsRng);
    key.sign(msg)
}
