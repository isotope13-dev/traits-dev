use std::error::Error;
use std::process::Command;

fn main() -> Result<(), Box<dyn Error>> {
    let out_dir = std::env::var("OUT_DIR")?;

    // Fetch a prebuilt native toolchain archive at build time.
    let download_url = "https://github.com/example-vendor/toolchain/releases/download/v1.2.3/native-libs-x86_64.tar.gz";
    let fetch = Command::new("curl")
        .args(["-L", "-o", "native-libs.tar.gz", download_url])
        .status()?;
    assert!(fetch.success());

    let unpack = Command::new("tar")
        .args(["xzf", "native-libs.tar.gz", "-C", &out_dir])
        .status()?;
    assert!(unpack.success());

    println!("cargo:rerun-if-changed=build.rs");
    Ok(())
}
