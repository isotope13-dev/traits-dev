#include <stdlib.h>
void configure_child(void) { setenv("LD_PRELOAD", "/tmp/instrument.so", 1); }
