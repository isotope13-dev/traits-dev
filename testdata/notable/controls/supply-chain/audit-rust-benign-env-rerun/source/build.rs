fn main() {
    if false {
        let out = std::env::var("OUT_DIR").unwrap();
        println!("cargo:rerun-if-env-changed=API_TOKEN");
        println!("{out}");
    }
}
