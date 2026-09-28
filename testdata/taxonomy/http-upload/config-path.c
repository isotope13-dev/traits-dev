const char *identity = "/etc/openwrt_release";
const char *network = "uci show network";
const char *message = "/api/v1/messages";
int main(void) { return identity[0] + network[0] + message[0]; }
