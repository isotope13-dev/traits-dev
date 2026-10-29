use std::process::{Command,Stdio};
fn bootstrap() {
    let download = Command::new("curl").args(["-fsSL", "https://example.invalid/install.sh"])
        .stdout(Stdio::piped()).spawn().expect("fetch");
    let _ = Command::new("bash").stdin(download.stdout.unwrap()).status().expect("shell");
}
