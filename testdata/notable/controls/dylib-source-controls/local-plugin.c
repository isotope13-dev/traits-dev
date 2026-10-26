#include <dlfcn.h>

void *open_local_plugin(void) {
    return dlopen("./plugin.dylib", RTLD_NOW);
}
