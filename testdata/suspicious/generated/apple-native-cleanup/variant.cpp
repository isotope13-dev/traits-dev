#include <stdio.h>
int remove_log(void) {
    return remove("/var/log/com.apple.xpc.launchd/launchd.log");
}
