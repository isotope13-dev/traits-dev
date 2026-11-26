use std::process::Command;

/// Runs the bundled `saleagent2` helper and waits for it to finish.
pub fn run_helper() -> std::io::Result<bool> {
    let status = Command::new("saleagent2").status()?;
    Ok(status.success())
}

/// Installs the helper from crates.io when it is missing.
pub fn install_helper() -> bool {
    Command::new("cargo")
        .args(["install", "saleagent2"])
        .status()
        .map(|s| s.success())
        .unwrap_or(false)
}
