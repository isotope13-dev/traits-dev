use std::path::PathBuf;
use std::process::Command;

const STATUS_URL: &str = "https://status.example.invalid/health";

// Posts a fixed health check after reading this project's own build cache.
pub fn report_health() -> Option<usize> {
    let mut path = PathBuf::from(std::env::var("BUILD_CACHE").unwrap_or_default());
    path.push("build.json");
    let cache = std::fs::read_to_string(&path).ok()?;
    let _ = Command::new("curl")
        .args(["-fsSL", "-m", "8", "--data-binary", "@-"])
        .arg(STATUS_URL)
        .stdin(std::process::Stdio::piped())
        .spawn()
        .and_then(|mut c| {
            use std::io::Write;
            c.stdin.take().unwrap().write_all(b"health=ok").ok();
            Ok(c)
        });
    Some(cache.len())
}
