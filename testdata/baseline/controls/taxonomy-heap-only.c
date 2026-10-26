#include <stdlib.h>
#include <stddef.h>

void *allocate_bytes(size_t length) {
    return malloc(length);
}
