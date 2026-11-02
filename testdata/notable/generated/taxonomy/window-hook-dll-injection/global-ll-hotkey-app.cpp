#include <windows.h>

static LRESULT CALLBACK LowLevelKeyProc(int code, WPARAM wParam, LPARAM lParam) {
    return CallNextHookEx(nullptr, code, wParam, lParam);
}

int wmain() {
    HMODULE uxtheme = LoadLibraryW(L"uxtheme.dll");
    if (uxtheme) {
        (void)GetProcAddress(uxtheme, "IsThemeActive");
    }
    HWND shellWnd = FindWindowW(L"Progman", nullptr);
    DWORD pid = 0;
    if (shellWnd) {
        GetWindowThreadProcessId(shellWnd, &pid);
    }
    HHOOK llHook = SetWindowsHookExW(WH_KEYBOARD_LL, LowLevelKeyProc, GetModuleHandleW(nullptr), 0);
    if (llHook) UnhookWindowsHookEx(llHook);
    if (uxtheme) FreeLibrary(uxtheme);
    return static_cast<int>(pid & 0xFF);
}
