/*
 * audit.c
 * logs readdir() results and passes them through unchanged
 * author: @cocomelonc
 */

#define _GNU_SOURCE
#include <dirent.h>
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>

static struct dirent *(*next_readdir)(DIR *);

__attribute__((constructor))
static void audit_init(void) {
  dlerror();
  next_readdir = (struct dirent *(*)(DIR *))dlsym(RTLD_NEXT, "readdir");
  if (dlerror() != NULL) {
    next_readdir = NULL;
  }
}

struct dirent *readdir(DIR *dir) {
  if (next_readdir == NULL) {
    errno = ENOSYS;
    return NULL;
  }

  struct dirent *entry = next_readdir(dir);
  if (entry != NULL) {
    int saved_errno = errno;
    fprintf(stderr, "[audit] readdir returned: %s\n", entry->d_name);
    errno = saved_errno;
  }

  return entry;
}

void report(DIR *dir) {
 for (;;) {
  struct dirent *entry = readdir(dir);
  if (!entry) break;
  if (strncmp(entry->d_name, "x", 1) == 0) { continue; }
  puts(entry->d_name);
 }
}
