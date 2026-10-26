#include <sys/socket.h>
#include <stdio.h>

#ifdef WITH_LSQUIC_IMPORT
extern int lsquic_engine_connect(void *, const void *, unsigned int, void *, void *);
#endif

int main(void) {
    puts("packets sent: 100");
#ifdef WITH_TARGET_USAGE
    puts("usage: <target ip> <target port>");
#endif
#ifdef WITH_SOCKET
    (void)socket(AF_INET, SOCK_STREAM, 0);
#endif
#ifdef WITH_LSQUIC_IMPORT
    (void)lsquic_engine_connect(0, 0, 0, 0, 0);
#endif
    return 0;
}
