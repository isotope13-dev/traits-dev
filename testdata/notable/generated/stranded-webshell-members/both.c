#include <string.h>
int inspect(const char *a, const char *b) {
    return strncmp(a, b, 8) && strchr(a, ':') != 0;
}
