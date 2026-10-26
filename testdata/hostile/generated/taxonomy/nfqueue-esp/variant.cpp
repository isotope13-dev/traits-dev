// Source-shape regression excerpt, not an executable exploit.
#include <sched.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/netfilter/nfnetlink_queue.h>
#include <linux/tc_act/tc_pedit.h>
#include <linux/tc_act/tc_mirred.h>
void setup(int source, int dest) {
    unshare(CLONE_NEWUSER | CLONE_NEWNET);
    const char *kind = "nlmon";
    const char *state[] = { "ip", "xfrm", "state", "add", "src", "::1",
                           "dst", "::1", "proto", "esp", "spi", "256" };
    int copy_mode = NFQNL_COPY_PACKET;
    int edit_attribute = TCA_PEDIT_PARMS;
    int redirect_action = TCA_EGRESS_REDIR;
    splice(source, nullptr, dest, nullptr, 64, 0);
}
