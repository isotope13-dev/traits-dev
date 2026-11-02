// Synthetic positive: remote RWX codecave with renamed locals.
// Exercises source-remote-rwx-write-profile without the suspended-child
// staging half (this file spawns nothing and suspends nothing).
#include <windows.h>

DWORD stage_blob_into_target(HANDLE target_handle, const void *payload,
                             SIZE_T payload_len) {
    LPVOID remote_base = VirtualAllocEx(target_handle, NULL, payload_len,
                                        MEM_COMMIT | MEM_RESERVE,
                                        PAGE_EXECUTE_READWRITE);
    if (!remote_base) {
        return 1;
    }
    SIZE_T bytes_done = 0;
    if (!WriteProcessMemory(target_handle, remote_base, payload, payload_len,
                            &bytes_done)) {
        return 2;
    }
    FlushInstructionCache(target_handle, remote_base, payload_len);
    HANDLE worker = CreateRemoteThread(target_handle, NULL, 0,
                                       (LPTHREAD_START_ROUTINE)remote_base,
                                       NULL, 0, NULL);
    if (!worker) {
        return 3;
    }
    WaitForSingleObject(worker, INFINITE);
    DWORD exit_code = 0;
    GetExitCodeThread(worker, &exit_code);
    CloseHandle(worker);
    VirtualFreeEx(target_handle, remote_base, 0, MEM_RELEASE);
    return exit_code;
}
