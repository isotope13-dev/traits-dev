use std::process::Command;
fn main() {
    // Command::new("curl").arg("--insecure");
    let _ = Command::new("curl").arg("https://localhost/").output();
}
