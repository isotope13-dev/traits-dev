#include <stdio.h>
static const char *roles[] = { "root", "admin", "guest", "password", "user", NULL };
int check(const char *u, const char *p) { return strcmp(u, "admin") == 0; }
