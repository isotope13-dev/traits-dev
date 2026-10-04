#include <sys/mman.h>
#include <stddef.h>

int main(void) {
    void *address = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                         MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (address == MAP_FAILED) return 1;
    return munmap(address, 4096);
}
