#include <stdio.h>
void paths(int pid) {
  char a[64], b[64], c[64];
  snprintf(a, sizeof(a), "/proc/%d/cmdline", pid);
  snprintf(b, sizeof(b), "/proc/%d/maps", pid);
  snprintf(c, sizeof(c), "/proc/%d/mem", pid);
}
