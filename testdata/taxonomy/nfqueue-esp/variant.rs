// Source-shape regression excerpt, not an executable exploit.
const NFQNL_COPY_PACKET: u8 = 2;
const TCA_PEDIT_PARMS: u16 = 2;
const TCA_EGRESS_REDIR: i32 = 1;
fn setup(fd: i32, pipe: i32) {
    unsafe { libc::unshare(libc::CLONE_NEWUSER | libc::CLONE_NEWNET); }
    let link = ["ip", "link", "add", "monitor8", "type", "nlmon"];
    let sa = ["ip", "xfrm", "state", "add", "src", "127.0.0.1",
              "dst", "127.0.0.1", "proto", "esp", "spi", "256"];
    let queue_mode = NFQNL_COPY_PACKET;
    let edit = TCA_PEDIT_PARMS;
    let redirect = TCA_EGRESS_REDIR;
    unsafe { libc::splice(pipe, std::ptr::null_mut(), fd, std::ptr::null_mut(), 64, 0); }
}
