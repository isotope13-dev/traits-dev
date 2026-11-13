// Benign control: `@loader_path` is the standard macOS rpath token that
// every dylib build script emits. It shares the `loader_path` substring
// with staging-path naming vocabulary but is linker syntax, not payload
// staging; the staging-path name trait must not fire on it.
use std::env;

fn main() {
    let target = env::var("TARGET").unwrap();
    if target.contains("darwin") {
        println!("cargo:rustc-link-arg=-Wl,-rpath,@loader_path");
        println!("cargo:rustc-link-arg=-Wl,-rpath,@loader_path/.");
    } else if target.contains("windows") {
        println!("cargo:rustc-link-search=native={}", env::var("OUT_DIR").unwrap());
    } else {
        println!("cargo:rustc-link-arg=-Wl,-rpath,$ORIGIN");
    }
    println!("cargo:rerun-if-changed=build.rs");
}
