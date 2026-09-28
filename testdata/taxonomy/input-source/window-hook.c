#include <windows.h>
LRESULT CALLBACK window_event(int code, WPARAM kind, LPARAM payload) {
    return CallNextHookEx(NULL, code, kind, payload);
}
void observe_window_messages(void) {
    HHOOK hook = SetWindowsHookExW(WH_CALLWNDPROC, window_event, NULL, GetCurrentThreadId());
    UnhookWindowsHookEx(hook);
}
