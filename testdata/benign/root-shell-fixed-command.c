#include <unistd.h>
int main(void){setuid(0);execl("/bin/bash", "bash", "-c", "id", (char *)NULL);return 0;}
