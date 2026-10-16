#include <sys/socket.h>
#include <string.h>
void save(int fd) {
    const char *commands[] = {
        "CONFIG SET dir /var/lib/redis\r\n",
        "CONFIG SET dbfilename dump.rdb\r\n",
        "SAVE\r\n"
    };
    for (int i = 0; i < 3; i++) send(fd, commands[i], strlen(commands[i]), 0);
}
