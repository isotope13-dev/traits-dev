use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());
    let version = env!("CARGO_PKG_VERSION");

    // The expected digest comes from the checksum trust-anchor file
    // shipped in the crate; a missing entry refuses the download.
    let expected = lookup_checksum(
        include_str!("sidecar-checksums.json"),
        version,
        "tool-linux-amd64",
    )
    .expect("pinned checksum required");

    let url = format!(
        "https://github.com/example/tool/releases/download/tool-v{version}/tool-linux-amd64"
    );
    let dest = out_dir.join("tool");
    download(&url, &dest, &expected).expect("verified download");
}

fn download(
    url: &str,
    dest: &PathBuf,
    expected_sha256: &str,
) -> Result<(), Box<dyn std::error::Error>> {
    let response = ureq::get(url).call()?;
    if response.status() != 200 {
        return Err(format!("HTTP {} from {url}", response.status()).into());
    }
    let mut reader = response.into_body().into_reader();
    let mut bytes = Vec::new();
    std::io::Read::read_to_end(&mut reader, &mut bytes)?;

    // Integrity gate runs before the bytes are written anywhere.
    verify_sha256(&bytes, expected_sha256)?;
    fs::write(dest, &bytes)?;
    Ok(())
}

fn lookup_checksum(json: &str, version: &str, asset: &str) -> Option<String> {
    let map: serde_json::Value = serde_json::from_str(json).ok()?;
    map.get(version)?
        .get(asset)?
        .as_str()
        .map(str::to_string)
}

fn verify_sha256(bytes: &[u8], expected_hex: &str) -> Result<(), String> {
    let actual = sha256_hex(bytes);
    if actual.eq_ignore_ascii_case(expected_hex.trim()) {
        Ok(())
    } else {
        Err(format!("expected sha256 {expected_hex}, got {actual}"))
    }
}

fn sha256_hex(bytes: &[u8]) -> String {
    use sha2::{Digest, Sha256};
    let digest = Sha256::digest(bytes);
    let mut out = String::new();
    for byte in digest {
        out.push_str(&format!("{byte:02x}"));
    }
    out
}
