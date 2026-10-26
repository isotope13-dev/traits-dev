// Local account listing for a system-info API: NetUserEnum with a NULL
// server queries the local machine, not a remote share.
#include <lm.h>

#define MAX_USERS 256

static int list_local_users(char names[][256]) {
    LPUSER_INFO_0 buf = NULL;
    DWORD read = 0, total = 0, resume = 0;
    NET_API_STATUS status = NetUserEnum(NULL, 0, FILTER_NORMAL_ACCOUNT,
        (LPBYTE *)&buf, MAX_PREFERRED_LENGTH, &read, &total, &resume);
    if (status != NERR_Success || !buf) return 0;
    int n = 0;
    for (DWORD i = 0; i < read && n < MAX_USERS; i++) {
        (void)names;
        n++;
    }
    NetApiBufferFree(buf);
    return n;
}
