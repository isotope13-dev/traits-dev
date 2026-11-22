/* Wine debugger test shape: allocate RWX in a child it spawned, then write into it. */
#include <stdarg.h>
#include "windows.h"
#include "wine/test.h"

static void test_remote_rwx(void)
{
    PROCESS_INFORMATION pi;
    STARTUPINFOA si = { sizeof(si) };
    BYTE buf[16] = { 0 };
    void *mem;
    BOOL ret;

    ret = CreateProcessA(NULL, "cmd /c exit 0", NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
    ok(ret, "CreateProcess failed\n");
    mem = VirtualAllocEx(pi.hProcess, NULL, sizeof(buf), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    ok(mem != NULL, "VirtualAllocEx failed\n");
    ret = WriteProcessMemory(pi.hProcess, mem, buf, sizeof(buf), NULL);
    ok(ret, "WriteProcessMemory failed\n");
    TerminateProcess(pi.hProcess, 0);
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
}
