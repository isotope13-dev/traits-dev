#include <unistd.h>
#include <fcntl.h>

int main(void) {
    int output = open("session.log", O_CREAT | O_WRONLY, 0600);
    dup2(output, 1);
    char *args[] = {"/bin/sh", "-i", 0};
    execve("/bin/sh", args, 0);
    return 0;
}
