#include <windows.h>

void report_local_profile(void) {
    WCHAR image[MAX_PATH], computer[MAX_COMPUTERNAME_LENGTH + 1];
    WCHAR user[256], domain[256], logon_server[256];
    DWORD image_size = MAX_PATH, computer_size = MAX_COMPUTERNAME_LENGTH + 1;
    DWORD user_size = 256, domain_size = 256;
    OSVERSIONINFOW version = { sizeof(version) };

    GetModuleFileNameW(NULL, image, image_size);
    GetVersionExW(&version);
    GetComputerNameW(computer, &computer_size);
    GetUserNameW(user, &user_size);
    GetEnvironmentVariableW(L"USERDOMAIN", domain, domain_size);
    GetEnvironmentVariableW(L"LOGONSERVER", logon_server, domain_size);
}
