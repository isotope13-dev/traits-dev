#include <stdio.h>
#include <stdlib.h>

int main(void) {
  char path[128];
  /* The formatted path is unrelated to the fixed maintenance command. */
  snprintf(path, sizeof path, "%s/report.txt", "/tmp"); system("printf 'ready' >/dev/null");
  return path[0] == '\0';
}
