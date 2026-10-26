#include <dlfcn.h>
int main(void) { return dlsym(RTLD_DEFAULT, "puts") == 0; }
