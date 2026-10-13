use std::os::unix::process::CommandExt;
fn main() {
    let mut child = std::process::Command::new("/bin/true");
    unsafe { child.pre_exec(|| Ok(())); }
}
