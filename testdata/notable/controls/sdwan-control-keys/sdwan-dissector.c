#define _GNU_SOURCE
#include <string.h>
int has_key_fields(const void *buffer, unsigned long size) {
    return memmem(buffer, size, "\x40\x03\x06", 3) &&
           memmem(buffer, size, "\x40\x0c\x04", 3) &&
           memmem(buffer, size, "\x05\x01\x0c\x06\x40", 5);
}
