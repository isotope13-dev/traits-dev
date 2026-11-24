void format(char *buf, const char *host) {
 snprintf(buf, 512, "ping -n 1 -w 300 %s", host);
 snprintf(buf, 512, "ping -c 1 -s 64 %s", host);
}
