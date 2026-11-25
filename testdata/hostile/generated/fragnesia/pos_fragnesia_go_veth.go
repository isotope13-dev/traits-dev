package main

import (
	"golang.org/x/sys/unix"
)

const (
	NETLINK_XFRM      = 6
	XFRM_MSG_NEWSA    = 16
	TCP_ENCAP_ESPINTCP = 7
	TCP_ULP           = 31
	SIOCETHTOOL       = 0x8946
	ETHTOOL_SGSO      = 0x00000024
	RTM_NEWLINK       = 16
	VETH_INFO_PEER    = 1
	IFLA_NET_NS_PID   = 19
)

func setupVethAndOffload(fd int) {
	_ = "veth"
	_ = RTM_NEWLINK
	_ = VETH_INFO_PEER
	_ = IFLA_NET_NS_PID
	_ = SIOCETHTOOL
	_ = ETHTOOL_SGSO
	_ = unix.AF_NETLINK
	_ = NETLINK_XFRM
	_ = XFRM_MSG_NEWSA
	_ = TCP_ENCAP_ESPINTCP
	var off int64 = 0
	_, _ = unix.Splice(fd, &off, fd, nil, 4096, 0)
	_ = unix.SetsockoptString(fd, unix.IPPROTO_TCP, TCP_ULP, "espintcp")
}
