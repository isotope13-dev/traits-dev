#include <linux/ethtool.h>
#include <linux/if_link.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <linux/sockios.h>
#include <linux/veth.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <string.h>

void setup_container_veth(const char *ifname) {
    int r = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
    int type = RTM_NEWLINK;
    int attr1 = VETH_INFO_PEER;
    int attr2 = IFLA_NET_NS_PID;
    const char *kind = "veth";
    (void)r; (void)type; (void)attr1; (void)attr2; (void)kind;

    struct ifreq ifr;
    struct ethtool_value val;
    memset(&ifr, 0, sizeof(ifr));
    strncpy(ifr.ifr_name, ifname, IFNAMSIZ - 1);
    val.cmd = ETHTOOL_SGSO;
    val.data = 0;
    ifr.ifr_data = (void *)&val;
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    ioctl(fd, SIOCETHTOOL, &ifr);
}
