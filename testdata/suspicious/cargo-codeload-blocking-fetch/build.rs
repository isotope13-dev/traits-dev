// Build-time third-party source fetch: blocking reqwest client plus a
// codeload.github.com archive URL. Regression fixture for the codeload
// archive-URL trait and the blocking-Client builder spelling; together
// these make the external-artifact-download build-script suspicion fire.
use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());
    let tag = env::var("EXAMPLE_LIB_VERSION").unwrap_or_else(|_| "v1.2.3".to_string());
    let url = format!(
        "https://codeload.github.com/example-org/example-lib/zip/refs/tags/{tag}"
    );

    let client = reqwest::blocking::Client::builder()
        .timeout(std::time::Duration::from_secs(120))
        .build()
        .expect("failed to build HTTP client");

    let mut attempts = 0;
    let bytes = loop {
        attempts += 1;
        match client.get(&url).send() {
            Ok(resp) if resp.status().is_success() => break resp.bytes().expect("response body"),
            _ if attempts < 5 => {
                std::thread::sleep(std::time::Duration::from_secs(2 << attempts));
            }
            _ => panic!("Failed to download example-lib from {url} after {attempts} attempts"),
        }
    };

    let archive = out_dir.join("example-lib.zip");
    fs::write(&archive, bytes).expect("failed to write downloaded archive");
    println!("cargo:rerun-if-changed=build.rs");
}
