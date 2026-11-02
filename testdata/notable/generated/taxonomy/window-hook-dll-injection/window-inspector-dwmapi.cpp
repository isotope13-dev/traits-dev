#include <windows.h>

int wmain() {
    HMODULE dwm = LoadLibraryA("dwmapi.dll");
    if (dwm) {
        (void)GetProcAddress(dwm, "DwmSetWindowAttribute");
    }
    HWND hwnd = FindWindowW(L"Shell_TrayWnd", nullptr);
    if (hwnd) {
        DWORD tid = GetWindowThreadProcessId(hwnd, nullptr);
        PostThreadMessageW(tid, WM_NULL, 0, 0);
    }
    if (dwm) FreeLibrary(dwm);
    return 0;
}
