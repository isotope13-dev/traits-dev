static int check_session_cookie(const wchar_t *host, const wchar_t *path, const wchar_t *cookie_hdr, char *out, size_t out_sz) {
    HINTERNET hSession = WinHttpOpen(L"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                                     WINHTTP_ACCESS_TYPE_NO_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
    if (!hSession) return -1;
    HINTERNET hConn = WinHttpConnect(hSession, host, INTERNET_DEFAULT_HTTPS_PORT, 0);
    if (!hConn) {
        WinHttpCloseHandle(hSession);
        return -1;
    }
    HINTERNET hReq = WinHttpOpenRequest(hConn, L"GET", path, NULL,
                                        WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES,
                                        WINHTTP_FLAG_SECURE);
    if (hReq) {
        if (WinHttpSendRequest(hReq, cookie_hdr, (DWORD)-1L, WINHTTP_NO_REQUEST_DATA, 0, 0, 0) &&
            WinHttpReceiveResponse(hReq, NULL)) {
            DWORD n = 0;
            WinHttpReadData(hReq, out, (DWORD)(out_sz - 1), &n);
            out[n] = '\0';
        }
        WinHttpCloseHandle(hReq);
    }
    WinHttpCloseHandle(hConn);
    WinHttpCloseHandle(hSession);
    return 0;
}

void check_user_sessions(const wchar_t *chatgpt_tok, const wchar_t *claude_key, const wchar_t *cursor_tok) {
    wchar_t hdr[1024];
    char resp[4096];

    swprintf(hdr, 1024, L"Cookie: __Secure-next-auth.session-token.0=%ls\r\n", chatgpt_tok);
    check_session_cookie(L"chatgpt.com", L"/api/auth/session", hdr, resp, sizeof(resp));
    check_session_cookie(L"chatgpt.com", L"/backend-api/me", hdr, resp, sizeof(resp));

    swprintf(hdr, 1024, L"Cookie: sessionKey=%ls\r\n", claude_key);
    check_session_cookie(L"claude.ai", L"/api/auth/current_account", hdr, resp, sizeof(resp));

    swprintf(hdr, 1024, L"Cookie: WorkosCursorSessionToken=%ls\r\n", cursor_tok);
    check_session_cookie(L"www.cursor.com", L"/api/auth/me", hdr, resp, sizeof(resp));
}
