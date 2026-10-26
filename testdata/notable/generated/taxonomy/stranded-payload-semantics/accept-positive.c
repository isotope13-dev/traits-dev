#include <sys/socket.h>
int run(int fd) { return accept(fd, 0, 0); }
