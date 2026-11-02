#include <linux/ethtool_netlink.h>
#include <linux/genetlink.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <net/if.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int configure_nic_offload(const char *ifname)
{
	int rt = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
	int gn = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
	unsigned int idx = if_nametoindex(ifname);
	const char *family = ETHTOOL_GENL_NAME;
	int cmd = ETHTOOL_MSG_FEATURES_SET;

	if (rt < 0 || gn < 0 || idx == 0) {
		if (rt >= 0)
			close(rt);
		if (gn >= 0)
			close(gn);
		return -1;
	}
	printf("configuring %s (index %u) via %s cmd=%d\n", ifname, idx, family, cmd);
	close(rt);
	close(gn);
	return 0;
}

int main(void)
{
	return configure_nic_offload("eth0");
}
