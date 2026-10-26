#include <string.h>
int transform(char *a, char *b, unsigned n) { memmove(a, b, n); memset(b, 65, n); return memcmp(a, b, n); }
