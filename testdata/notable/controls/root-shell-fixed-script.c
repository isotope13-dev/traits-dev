#include <unistd.h>
int main(void){setuid(0);execl("/bin/sh", "sh", "/usr/libexec/maintenance.sh", (char *)NULL);return 0;}
