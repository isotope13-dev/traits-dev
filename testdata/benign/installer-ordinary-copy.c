#include <windows.h>
BOOL backup(void) {
    return CopyFileW(L"C:\\Config.Msi\\old.rbs", L"C:\\backup\\old.rbs", TRUE);
}
