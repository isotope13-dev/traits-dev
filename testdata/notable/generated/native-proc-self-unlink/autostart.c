#include <unistd.h>
void startup(int enabled) {
    if (!enabled) {
        unlink("/home/user/.config/autostart/application.desktop");
    } else {
        char executable[4096] = {0};
        readlink("/proc/self/exe", executable, sizeof(executable) - 1);
        write_desktop_entry(executable);
    }
}
