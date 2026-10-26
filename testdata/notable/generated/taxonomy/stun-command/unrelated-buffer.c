#include <sys/socket.h>
#include <stdlib.h>
int status_message(int fd) {
    char message[128];
    int n;
    n = recvfrom(fd, message, sizeof message, 0, 0, 0);
    if (n <= 0) return 1;
    return system("logger network-status");
}
