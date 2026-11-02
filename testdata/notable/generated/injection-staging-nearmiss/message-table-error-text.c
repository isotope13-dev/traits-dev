// Benign positive: reads the ntdll message table to format an error string.
// Exercises source-pe-resource-access without any loader-staging context,
// so no resource-stage hostile composite may fire.
#include <windows.h>

const wchar_t *describe_nt_error(DWORD status) {
    static wchar_t text[512];
    HMODULE ntdll = GetModuleHandleW(L"ntdll.dll");
    HRSRC table = FindResourceExW(ntdll, (LPCWSTR)RT_MESSAGETABLE,
                                  MAKEINTRESOURCEW(1), 0);
    if (!table) {
        return L"unknown";
    }
    HGLOBAL loaded = LoadResource(ntdll, table);
    const void *locked = LockResource(loaded);
    DWORD bytes = SizeofResource(ntdll, table);
    if (!locked || !bytes) {
        return L"unknown";
    }
    FormatMessageW(FORMAT_MESSAGE_FROM_HMODULE | FORMAT_MESSAGE_IGNORE_INSERTS,
                   ntdll, status, 0, text, 512, NULL);
    return text;
}
