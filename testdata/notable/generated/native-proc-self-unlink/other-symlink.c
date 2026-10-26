#include <unistd.h>
void cleanup_link(void) {
    char target[4096] = {0};
    readlink("/proc/self/cwd", target, sizeof(target) - 1);
    unlink(target);
}
