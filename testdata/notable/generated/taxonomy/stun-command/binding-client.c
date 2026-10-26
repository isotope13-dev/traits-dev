#include <sys/socket.h>
void discover(int fd, struct sockaddr *peer, socklen_t size) {
    unsigned char packet[20] = {0x00,0x01,0x00,0x00,0x21,0x12,0xa4,0x42,0,0,0,0,0,0,0,0,0,0,0,0};
    sendto(fd, packet, sizeof packet, 0, peer, size);
    recvfrom(fd, packet, sizeof packet, 0, 0, 0);
}
