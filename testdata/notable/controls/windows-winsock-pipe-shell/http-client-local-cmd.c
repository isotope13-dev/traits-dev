#include <winsock2.h>
#include <windows.h>
#include <stdio.h>
#include <string.h>

int fetch_status(const char *host_ip, int port, char *resp, int cap) {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);
    SOCKET s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    struct sockaddr_in srv = {0};
    srv.sin_family = AF_INET;
    srv.sin_port = htons((u_short)port);
    srv.sin_addr.s_addr = inet_addr(host_ip);
    if (connect(s, (struct sockaddr *)&srv, sizeof(srv)) != 0) {
        closesocket(s);
        return -1;
    }
    const char *req = "GET /healthz HTTP/1.0\r\n\r\n";
    send(s, req, (int)strlen(req), 0);
    int total = 0, n;
    while ((n = recv(s, resp + total, cap - 1 - total, 0)) > 0) {
        total += n;
        if (total >= cap - 1) break;
    }
    resp[total] = '\0';
    closesocket(s);
    return total;
}

int capture_local_tool_version(const char *subcmd, char *out, int cap) {
    SECURITY_ATTRIBUTES sa = { sizeof(sa), NULL, TRUE };
    HANDLE rd, wr;
    if (!CreatePipe(&rd, &wr, &sa, 0)) return -1;
    SetHandleInformation(rd, HANDLE_FLAG_INHERIT, 0);

    STARTUPINFOA si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE;
    si.hStdOutput = wr;
    si.hStdError = wr;

    char cmd[512];
    snprintf(cmd, sizeof(cmd), "cmd.exe /c \"%s\"", subcmd);
    BOOL ok = CreateProcessA(NULL, cmd, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
    CloseHandle(wr);
    int total = 0;
    if (ok) {
        char buf[512];
        DWORD nr = 0;
        while (ReadFile(rd, buf, sizeof(buf), &nr, NULL) && nr > 0) {
            if (total + (int)nr < cap - 1) {
                memcpy(out + total, buf, nr);
                total += (int)nr;
            }
        }
        WaitForSingleObject(pi.hProcess, 2000);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }
    CloseHandle(rd);
    out[total] = '\0';
    return total;
}

int main(void) {
    char http_buf[1024];
    char ver_buf[1024];
    fetch_status("198.51.100.50", 80, http_buf, sizeof(http_buf));
    capture_local_tool_version("ver", ver_buf, sizeof(ver_buf));
    printf("health=%s ver=%s\n", http_buf, ver_buf);
    return 0;
}
