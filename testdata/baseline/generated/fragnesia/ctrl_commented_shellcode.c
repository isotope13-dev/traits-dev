#include <stdio.h>

/*
 * Example shellcode documentation (NOT executable code):
 * 0xb0, 0x69, 0x0f, 0x05,
 * 0x6a, 0x3b, 0x58, 0x0f, 0x05
 */
int main(void) {
    puts("documentation only");
    return 0;
}
