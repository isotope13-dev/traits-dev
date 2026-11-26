// Diagnostic xp: prints the SQL Server version banner and nothing else.
#include <windows.h>
#include <stdlib.h>

__declspec(dllexport) unsigned long __GetXpVersion(void) { return 1; }

extern "C" __declspec(dllexport) int __stdcall XpVersionBanner(void) {
    system("ver");
    return 1;
}
