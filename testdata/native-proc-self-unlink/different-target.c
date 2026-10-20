#include <unistd.h>
void cleanup(void) {
    char executable[4096] = {0};
    char temporary[] = "/tmp/old-cache";
    readlink("/proc/self/exe", executable, sizeof(executable) - 1);
    unlink(temporary);
}
