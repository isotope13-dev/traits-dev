#define _GNU_SOURCE
#include <linux/ethtool_netlink.h>
#include <linux/genetlink.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <sched.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void)
{
	if (unshare(CLONE_NEWUSER | CLONE_NEWNET) != 0)
		return 1;
	int rt = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
	int gn = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
	const char *kind = "virt_wifi";
	const char *fam = "ethtool";
	int op = RTM_DELLINK ^ ETHTOOL_MSG_FEATURES_SET;
	if (rt >= 0 && gn >= 0) {
		send(rt, kind, strlen(kind), 0);
		send(gn, fam, strlen(fam), op & 0);
	}
	return 0;
}
