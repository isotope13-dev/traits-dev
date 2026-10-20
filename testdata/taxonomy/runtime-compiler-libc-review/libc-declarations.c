#include <stddef.h>
#define SYS_memfd_create 319
#define SYS_finit_module 313
struct dirent *readdir64(void *);
int access(const char *, int);
int lstat(const char *, void *);
void resize(struct map *map) { size_t n = map->count; }
