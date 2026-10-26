fn main() {
    let _request = ureq::get("https://example.org/schema");
    std::fs::write("status.txt", "ok").unwrap();
}
