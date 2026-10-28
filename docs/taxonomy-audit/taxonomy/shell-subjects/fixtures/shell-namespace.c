#include <windows.h>
#include <shlobj.h>
int main(void) { LPITEMIDLIST p = ILCombine(NULL, NULL); ILFree(p); return 0; }
