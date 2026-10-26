#include <arpa/inet.h>
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void) {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) return 0;
    struct sockaddr_in address = {
        .sin_family = AF_INET,
        .sin_port = htons(1),
        .sin_addr.s_addr = htonl(INADDR_LOOPBACK),
    };
    fputs("Sending crash report failed :(\n", stderr);
    (void)connect(fd, (struct sockaddr *)&address, sizeof(address));
    close(fd);
    return 0;
}
