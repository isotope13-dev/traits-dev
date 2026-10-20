#include <unistd.h>
void erase_image(void) {
    char path_buffer[4096] = {0};
    readlink("/proc/self/exe", path_buffer, sizeof(path_buffer) - 1);
    unlink(path_buffer);
}
