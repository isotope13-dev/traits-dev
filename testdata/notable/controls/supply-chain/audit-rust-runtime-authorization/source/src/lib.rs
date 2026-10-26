pub fn operate() {
    if false {
        let token = std::env::var("API_TOKEN").unwrap_or_default();
        let _ = reqwest::blocking::Client::new().get("https://service.example.invalid/status").bearer_auth(token).send();
    }
}
