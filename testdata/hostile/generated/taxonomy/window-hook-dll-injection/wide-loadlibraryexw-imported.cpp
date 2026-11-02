#include <windows.h>

int wmain(int argc, wchar_t** argv) {
    if (argc < 2) return 1;
    HWND hwnd = FindWindowW(L"UnityWndClass", nullptr);
    if (!hwnd) return 2;
    DWORD tid = GetWindowThreadProcessId(hwnd, nullptr);
    if (!tid) return 3;

    HMODULE mod = LoadLibraryExW(argv[1], nullptr, DONT_RESOLVE_DLL_REFERENCES);
    if (!mod) return 4;
    HOOKPROC cb = reinterpret_cast<HOOKPROC>(GetProcAddress(mod, "NextHookProc"));
    if (!cb) {
        FreeLibrary(mod);
        return 5;
    }

    HHOOK hook = SetWindowsHookExW(WH_GETMESSAGE, cb, mod, tid);
    if (!hook) {
        FreeLibrary(mod);
        return 6;
    }
    PostThreadMessageW(tid, WM_NULL, 0, 0);
    Sleep(250);
    UnhookWindowsHookEx(hook);
    FreeLibrary(mod);
    return 0;
}
