use std::process::Command;

pub fn update_tool() {
    let _ = Command::new("cargo")
        .args(["install", "--git", "https://example.invalid/tool.git"])
        .status();
}
