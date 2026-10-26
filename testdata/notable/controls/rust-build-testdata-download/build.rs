// Regression guard: reading OUT_DIR and downloading a pinned test-data
// file is build orchestration, not environment exfiltration.
use std::process::Command;

fn main() {
    let url = "https://example.com/testdata/v1/vectors.json";
    let out_dir = std::env::var("OUT_DIR").unwrap();
    let dest = std::path::Path::new(&out_dir).join("vectors.json");
    let status = Command::new("curl")
        .args(&["-L", url, "--retry", "3"])
        .arg("-o")
        .arg(dest)
        .status()
        .expect("failed to fetch test vectors");
    assert!(status.success());
}
