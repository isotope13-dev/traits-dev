#include <stdio.h>
#include <syslog.h>

int main(void) {
    openlog("sample", LOG_PID, LOG_USER);
    syslog(LOG_INFO, "this sample does nothing");
    closelog();
    return 0;
}
