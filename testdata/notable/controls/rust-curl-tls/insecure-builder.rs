use std::process::Command;
fn main() {
    let _ = Command::new("curl").arg("--insecure").arg("https://localhost/").output();
}
