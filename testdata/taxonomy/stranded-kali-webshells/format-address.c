#include <arpa/inet.h>
const char *format(struct in_addr addr) { return inet_ntoa(addr); }
