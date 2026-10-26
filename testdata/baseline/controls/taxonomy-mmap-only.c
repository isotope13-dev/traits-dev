#include <sys/mman.h>
#include <stddef.h>

void *map_page(void) {
    return mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
}
