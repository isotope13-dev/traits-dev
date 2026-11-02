// Synthetic positive: suspended spawn with RW (non-X) staging, executable
// rights granted later via VirtualProtectEx. Exercises
// suspended-remote-executable-staging without the RWX-codecave profile
// (no PAGE_EXECUTE_READWRITE allocation here).
#include <windows.h>

void launch_stalled_app(LPCWSTR app_path) {
    STARTUPINFOW startup_info;
    PROCESS_INFORMATION child_info;
    memset(&startup_info, 0, sizeof(startup_info));
    startup_info.cb = sizeof(startup_info);
    CreateProcessW(app_path, NULL, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL,
                   NULL, &startup_info, &child_info);
    SIZE_T region_len = 8192;
    LPVOID staging = VirtualAllocEx(child_info.hProcess, NULL, region_len,
                                    MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    char seed[128] = {0};
    WriteProcessMemory(child_info.hProcess, staging, seed, sizeof(seed),
                       NULL);
    DWORD previous = 0;
    VirtualProtectEx(child_info.hProcess, staging, region_len, PAGE_EXECUTE_READ, &previous);
    ResumeThread(child_info.hThread);
}
