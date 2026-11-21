#include <stdio.h>
void inspect(void) { popen("cat /proc/kallsyms | grep sys_getuid", "r"); }
