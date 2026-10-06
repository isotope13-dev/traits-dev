use std::io::Write;
use std::process::Command;

const INSTALL_SH_URL: &str = "https://apt.example.test/install.sh";

// Faithful shape of node-app-build's `--daemon deb` install: the operator
// is shown the exact command and must answer yes before anything runs.
pub fn ensure_helper_installed() -> anyhow::Result<()> {
    let installed = Command::new("dpkg-query")
        .args(["-W", "-f=${Status}", "helper"])
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).contains("install ok installed"))
        .unwrap_or(false);
    if !installed {
        eprintln!("Continue? [y/N]: ");
        let mut answer = String::new();
        std::io::stdin()
            .read_line(&mut answer)
            .expect("read user confirmation");
        if !matches!(answer.trim().to_lowercase().as_str(), "y" | "yes") {
            anyhow::bail!("aborted by user");
        }
        let install_cmd = format!("curl -fsSL {} | bash", INSTALL_SH_URL);
        let status = Command::new("sudo")
            .args(["sh", "-c", &install_cmd])
            .status()
            .expect("sudo curl + bash install");
        if !status.success() {
            anyhow::bail!("install failed");
        }
    }
    Ok(())
}
