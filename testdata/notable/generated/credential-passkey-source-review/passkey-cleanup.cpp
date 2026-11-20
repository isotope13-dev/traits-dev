#include <windows.h>
const char* field = "security_domain_secret";
const wchar_t* path = L"Google\\Chrome\\User Data\\Default\\passkey_enclave_state";
void reset() { DeleteFileW(path); }
