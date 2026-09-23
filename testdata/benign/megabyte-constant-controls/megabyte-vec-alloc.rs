//! Scratch buffer helpers.
// See https://github.com/rust-lang/rust for the Vec API.
pub fn megabyte_scratch() -> Vec<u8> {
    vec![0u8; 1024 * 1024]
}
pub fn exact_scratch() -> Vec<u8> {
    vec![0u8; 1048576]
}
