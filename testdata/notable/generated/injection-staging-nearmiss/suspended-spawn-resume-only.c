// Benign near-miss: launches a child suspended and resumes it, but never
// touches another process's memory. Must not fire either staging profile.
#include <windows.h>

void restart_paused_tool(LPCWSTR tool_path) {
    STARTUPINFOW startup_info;
    PROCESS_INFORMATION child_info;
    memset(&startup_info, 0, sizeof(startup_info));
    startup_info.cb = sizeof(startup_info);
    if (!CreateProcessW(tool_path, NULL, NULL, NULL, FALSE, CREATE_SUSPENDED,
                        NULL, NULL, &startup_info, &child_info)) {
        return;
    }
    ResumeThread(child_info.hThread);
    WaitForSingleObject(child_info.hProcess, INFINITE);
    CloseHandle(child_info.hThread);
    CloseHandle(child_info.hProcess);
}
