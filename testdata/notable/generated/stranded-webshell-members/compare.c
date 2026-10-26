#include <string.h>
int compare(const char *a, const char *b) {
    return strncmp(a, b, 8);
}
