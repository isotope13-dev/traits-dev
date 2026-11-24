void format(char *buf, const char *base, int b) {
 snprintf(buf, 512, "ping -n 1 -w 300 %s%d", base, b);
 snprintf(buf, 512, "ping -c 1 -s %d %s", b, base);
}
