#include <sys/mman.h>
const char *permission_name = "PROT_EXEC";
void *mapping(void) { return mmap(0, 4096, PROT_READ | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0); }
int main(void) { return mapping() == MAP_FAILED; }
