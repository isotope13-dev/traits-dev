#include <sys/mman.h>
#include <sys/shm.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <net/if.h>
void configure(int fd, int segment, void *address, unsigned long length,
    struct ip_mreq *membership) {
    void *view = shmat(segment, 0, 0);
    void *mapped = mmap(0, length, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    msync(mapped, length, MS_SYNC);
    mprotect(address, length, PROT_READ | PROT_EXEC);
    int channel = socket(AF_INET, SOCK_DGRAM, 0);
    unsigned int index = if_nametoindex("lo0");
    int ttl = 1;
    setsockopt(channel, IPPROTO_IP, IP_MULTICAST_TTL, &ttl, sizeof(ttl));
    setsockopt(channel, IPPROTO_IP, IP_ADD_MEMBERSHIP, membership, sizeof(*membership));
    void (*entry)(void) = (void (*)(void))address;
}
