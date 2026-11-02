#include <windows.h>

typedef HHOOK (WINAPI *PFN_SetWindowsHookExA)(int, HOOKPROC, HINSTANCE, DWORD);
typedef BOOL (WINAPI *PFN_PostThreadMessageA)(DWORD, UINT, WPARAM, LPARAM);

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    HWND target = FindWindowA("Notepad", NULL);
    if (!target) return 2;
    DWORD remoteTid = GetWindowThreadProcessId(target, NULL);
    if (!remoteTid) return 3;

    HMODULE hUser32 = GetModuleHandleA("user32.dll");
    PFN_SetWindowsHookExA fnHook = (PFN_SetWindowsHookExA)GetProcAddress(hUser32, "SetWindowsHookExA");
    PFN_PostThreadMessageA fnPost = (PFN_PostThreadMessageA)GetProcAddress(hUser32, "PostThreadMessageA");
    if (!fnHook || !fnPost) return 4;

    HMODULE payload = LoadLibraryA(argv[1]);
    if (!payload) return 5;
    HOOKPROC fnEntry = (HOOKPROC)GetProcAddress(payload, "InstallCallback");
    if (!fnEntry) return 6;

    HHOOK h = fnHook(WH_GETMESSAGE, fnEntry, payload, remoteTid);
    if (!h) return 7;
    fnPost(remoteTid, WM_NULL, 0, 0);
    return 0;
}
