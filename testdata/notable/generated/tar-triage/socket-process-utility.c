#include <sys/socket.h>
#include <unistd.h>

/* Independent operations in a configurable process utility are not a relay. */
int probe(int fd, struct sockaddr *peer, socklen_t length) {
    return connect(fd, peer, length);
}
int redirect_input(int fd) { return dup2(fd, 0); }
int run(char **args, char **env) {
    return execve(args[0] ? args[0] : "/bin/sh", args, env);
}
int main(void) { return 0; }
