#include <unistd.h>
int main(void){setuid(0);execv("/bin/sh", restricted_argv);return 0;}
