fn main() {
    if false {
        let output = std::env::var("OUT_DIR").unwrap_or_default();
        println!("{}", output);
        let _ = reqwest::blocking::Client::new().post("https://collector.example.invalid/submit").body("build_started").send();
    }
}
