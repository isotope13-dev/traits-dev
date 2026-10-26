#include <sys/mman.h>
#include <sys/shm.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <net/if.h>
void configure(int fd, int segment, void *region, unsigned long span,
    struct ip_mreq *membership) {
    void *view = shmat(segment, 0, 0);
    void *mapping = mmap(0, span, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    msync(mapping, span, MS_SYNC);
    mprotect(region, span, PROT_READ | PROT_EXEC);
    int handle = socket(AF_INET, SOCK_DGRAM, 0);
    unsigned int index = if_nametoindex("lo0");
    int ttl = 1;
    setsockopt(handle, IPPROTO_IP, IP_MULTICAST_TTL, &ttl, sizeof(ttl));
    setsockopt(handle, IPPROTO_IP, IP_ADD_MEMBERSHIP, membership, sizeof(*membership));
    void (*entry)(void) = (void (*)(void))region;
}
