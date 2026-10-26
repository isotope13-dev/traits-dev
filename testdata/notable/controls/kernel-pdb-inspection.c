#include <windows.h>
#include <dbghelp.h>
void inspect(HANDLE process) {
    const char *names[] = {"PspCreateProcessNotifyRoutine", "PspCreateThreadNotifyRoutine", "PspLoadImageNotifyRoutine"};
    DWORD64 image = SymLoadModuleEx(process, NULL, "ntkrnlmp.pdb", NULL, 0, 0, NULL, 0);
    SYMBOL_INFO symbol;
    ULONG length;
    for (int i = 0; i < 3; i++) {
        SymFromName(process, names[i], &symbol);
        SymGetTypeInfo(process, image, symbol.TypeIndex, TI_GET_LENGTH, &length);
    }
}
