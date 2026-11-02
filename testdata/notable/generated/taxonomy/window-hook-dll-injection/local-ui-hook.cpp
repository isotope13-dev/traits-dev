#include <windows.h>

static LRESULT CALLBACK LocalCallWndProc(int code, WPARAM wParam, LPARAM lParam) {
    return CallNextHookEx(nullptr, code, wParam, lParam);
}

int wmain() {
    HMODULE dwm = LoadLibraryA("dwmapi.dll");
    if (dwm) {
        (void)GetProcAddress(dwm, "DwmSetWindowAttribute");
    }
    DWORD selfTid = GetCurrentThreadId();
    HHOOK hook = SetWindowsHookExW(WH_CALLWNDPROC, LocalCallWndProc, nullptr, selfTid);
    PostThreadMessageW(selfTid, WM_NULL, 0, 0);
    if (hook) UnhookWindowsHookEx(hook);
    if (dwm) FreeLibrary(dwm);
    return 0;
}
