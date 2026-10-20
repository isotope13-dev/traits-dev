#include <unistd.h>
#include <string.h>
void cleanup(void) {
    char executable[4096] = {0};
    readlink("/proc/self/exe", executable, sizeof(executable) - 1);
    strcpy(executable, "/tmp/old-cache");
    unlink(executable);
}
