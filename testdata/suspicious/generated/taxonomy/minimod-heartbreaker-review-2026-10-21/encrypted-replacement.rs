use aes_gcm::{Aes256Gcm, aead::Aead};
use std::{fs::{OpenOptions, rename}, io::Write};
// An explicitly selected file can be replaced with an encrypted representation.
fn replace_selected_file(cipher: &Aes256Gcm, nonce: &[u8], data: &[u8], path: &str) {
    let ciphertext = cipher.encrypt(nonce.into(), data).unwrap();
    let mut output = OpenOptions::new().write(true).truncate(true).open(path).unwrap();
    output.write_all(&ciphertext).unwrap();
    rename(path, "encrypted-output").unwrap();
}
fn regenerate() {
    let source = include_str!("main.rs");
    metacore::morph(&source, "manifest", "build", 15, "encryptor");
}
