#include <stdlib.h>
int main(void) { return getenv("LD_PRELOAD") != 0; }
