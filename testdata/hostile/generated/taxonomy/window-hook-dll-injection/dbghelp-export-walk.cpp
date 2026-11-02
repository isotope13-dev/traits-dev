#include <windows.h>
#include <dbghelp.h>
#include <cstring>

static const char* FirstNonDllMainExport(HMODULE hMod) {
    ULONG sz = 0;
    auto* exp = static_cast<PIMAGE_EXPORT_DIRECTORY>(
        ImageDirectoryEntryToData(hMod, TRUE, IMAGE_DIRECTORY_ENTRY_EXPORT, &sz));
    if (!exp || exp->NumberOfNames == 0) return nullptr;
    auto* names = reinterpret_cast<const DWORD*>(
        reinterpret_cast<const BYTE*>(hMod) + exp->AddressOfNames);
    for (DWORD i = 0; i < exp->NumberOfNames; ++i) {
        const char* sym = reinterpret_cast<const char*>(hMod) + names[i];
        if (std::strcmp(sym, "DllMain") != 0) return sym;
    }
    return nullptr;
}

extern "C" __declspec(dllexport) BOOL WINAPI StageWindowCbtHook(const wchar_t* dllPath, const wchar_t* cls) {
    HWND wnd = FindWindowExW(nullptr, nullptr, cls, nullptr);
    if (!wnd) return FALSE;
    DWORD tid = GetWindowThreadProcessId(wnd, nullptr);
    if (!tid) return FALSE;

    HMODULE mod = LoadLibraryW(dllPath);
    if (!mod) return FALSE;
    const char* exportName = FirstNonDllMainExport(mod);
    if (!exportName) return FALSE;
    auto cb = reinterpret_cast<HOOKPROC>(GetProcAddress(mod, exportName));
    if (!cb) return FALSE;

    HHOOK h = SetWindowsHookExW(WH_CBT, cb, mod, tid);
    return h != nullptr;
}
