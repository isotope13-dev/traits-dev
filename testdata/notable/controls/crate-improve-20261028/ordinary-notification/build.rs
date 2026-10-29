use std::process::Command;
fn main() {
    let token = std::env::var("TELEGRAM_BOT_TOKEN").unwrap();
    let url = format!("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=build_complete", token, 123456789);
    let _ = Command::new("curl").arg("-fsS").arg(&url).status();
}
