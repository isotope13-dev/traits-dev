// Benign near-miss: remote RW allocation plus cross-process write, but no
// executable memory anywhere (no RWX/RX constant, no VirtualProtectEx) and
// no suspended process. Must not fire either injection-staging profile.
#include <windows.h>

void mirror_settings_block(HANDLE helper, const void *settings,
                           SIZE_T settings_len) {
    LPVOID mirror = VirtualAllocEx(helper, NULL, settings_len,
                                   MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!mirror) {
        return;
    }
    WriteProcessMemory(helper, mirror, settings, settings_len, NULL);
    FlushInstructionCache(helper, mirror, settings_len);
    HANDLE worker = CreateRemoteThread(helper, NULL, 0,
                                       (LPTHREAD_START_ROUTINE)mirror, NULL,
                                       0, NULL);
    if (worker) {
        CloseHandle(worker);
    }
}
