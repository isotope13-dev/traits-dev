#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

/* Static fixture for a remote stdio sink. It never executes a command. */
int main(void) {
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in sa = {0};
    sa.sin_family = AF_INET;
    sa.sin_port = htons(9000);
    sa.sin_addr.s_addr = inet_addr("8.8.8.8");
    connect(s, (struct sockaddr *)&sa, sizeof(sa));
    dup2(s, 0);
    dup2(s, 1);
    dup2(s, 2);
    puts("status heartbeat");
    return 0;
}
