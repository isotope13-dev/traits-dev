// Benign control: runtime integrity checking of a downloaded ML model.
// This is the checksum-pinning vocabulary of the build-script verify
// composite (constant digest, streaming SHA-256, mismatch diagnostic), but
// in ordinary library source with no build script, so no build-staging
// finding may result from it.
use sha2::{Digest, Sha256};
use std::io::{BufReader, Read};
use std::path::{Path, PathBuf};

const MODEL_SHA256: &str = "6b742aebce6f0f7f71f747931ac7becfc7c96c51641e14943b291eeb334e7947";

pub fn verify_sha256(path: &Path, expected: &str, label: &str) -> Result<(), String> {
    let file = std::fs::File::open(path).map_err(|e| format!("open failed: {e}"))?;
    let mut reader = BufReader::with_capacity(64 * 1024, file);
    let mut hasher = Sha256::new();
    let mut buf = [0u8; 64 * 1024];
    loop {
        let n = reader.read(&mut buf).map_err(|e| format!("read failed: {e}"))?;
        if n == 0 {
            break;
        }
        hasher.update(&buf[..n]);
    }
    let hash_hex = hex::encode(hasher.finalize());
    if hash_hex != expected {
        return Err(format!("Checksum mismatch for {label}: expected {expected}, got {hash_hex}"));
    }
    Ok(())
}

pub fn cached_model(cache_dir: &Path) -> PathBuf {
    let model_path = cache_dir.join("doc-orientation.onnx");
    let _ = verify_sha256(&model_path, MODEL_SHA256, "doc_ori");
    model_path
}
