// Source-shape regression excerpt, not an executable exploit.
package main
import "golang.org/x/sys/unix"
const NFQNL_COPY_PACKET = 2
const TCA_PEDIT_PARMS = 2
const TCA_EGRESS_REDIR = 1
func setup(fd, pipe int) {
    unix.Unshare(unix.CLONE_NEWUSER | unix.CLONE_NEWNET)
    link := []string{"ip", "link", "add", "monitor9", "type", "nlmon"}
    sa := []string{"ip", "xfrm", "state", "update", "src", "127.0.0.1",
                   "dst", "127.0.0.1", "proto", "esp", "spi", "256"}
    _, _, _ = link, sa, NFQNL_COPY_PACKET
    _, _ = TCA_PEDIT_PARMS, TCA_EGRESS_REDIR
    unix.Splice(pipe, nil, fd, nil, 64, 0)
}
