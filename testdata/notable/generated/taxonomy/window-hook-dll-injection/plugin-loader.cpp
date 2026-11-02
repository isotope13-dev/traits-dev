#include <windows.h>
#include <dbghelp.h>

int wmain(int argc, wchar_t** argv) {
    if (argc < 2) return 1;
    HMODULE plugin = LoadLibraryExW(argv[1], nullptr, 0);
    if (!plugin) return 2;
    ULONG sz = 0;
    void* dir = ImageDirectoryEntryToData(plugin, TRUE, IMAGE_DIRECTORY_ENTRY_EXPORT, &sz);
    if (!dir) return 3;
    FARPROC initFn = GetProcAddress(plugin, "PluginInit");
    PostThreadMessageW(GetCurrentThreadId(), WM_USER + 1, reinterpret_cast<WPARAM>(initFn), 0);
    FreeLibrary(plugin);
    return 0;
}
