#include <stdlib.h>
void init(void) { char *flag = getenv("FEATURE"); flag = 0; if (flag == NULL) { return; } }
