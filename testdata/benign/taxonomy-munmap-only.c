#include <sys/mman.h>
#include <stddef.h>

int release_mapping(void *address, size_t length) {
    return munmap(address, length);
}
