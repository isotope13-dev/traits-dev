// Positive fixture: staging-path identifier vocabulary in code. The
// `payload_path` identifier (and a non-linker `loader_path`) is the naming
// evidence this trait records; prose mentions and the `@loader_path` rpath
// token must not match (see controls/rust-build-rpath-loader-token.rs).
use std::env;
use std::fs;
use std::path::PathBuf;

fn payload_path() -> PathBuf {
    let base = env::var("APPDATA").map(PathBuf::from).unwrap_or_else(|_| PathBuf::from("."));
    base.join("Local").join("svcupdate.bin")
}

fn loader_path() -> PathBuf {
    env::current_exe().expect("current exe")
}

fn main() {
    let staged = payload_path();
    if !staged.exists() {
        fs::copy(loader_path(), &staged).expect("stage payload");
    }
    let _ = fs::read(&staged);
}
