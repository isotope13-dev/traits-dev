#include <windows.h>
#define READ_MEMORY 0x80002028
void query(unsigned char *request, DWORD size) {
    HANDLE device = CreateFileA("\\\\.\\PdFwKrnl", GENERIC_READ, 0, NULL, OPEN_EXISTING, 0, NULL);
    unsigned char output[64]; DWORD returned;
    DeviceIoControl(device, READ_MEMORY, request, size, output, sizeof(output), &returned, NULL);
    CloseHandle(device);
}
