int inspect_login_traffic(void) {
    int device = open("/dev/nit", 0);
    int mode = NI_PROMISC;
    ioctl(device, NIOCBIND, 0);
    return IPPORT_TELNET + device + mode;
}
