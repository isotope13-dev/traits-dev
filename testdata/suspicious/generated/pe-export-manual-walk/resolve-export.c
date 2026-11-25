#include <windows.h>

FARPROC resolve_export(BYTE *base, DWORD dir_rva, const char *wanted) {
    IMAGE_EXPORT_DIRECTORY *exp = (IMAGE_EXPORT_DIRECTORY *)(base + dir_rva); DWORD *names = (DWORD *)(base + exp->AddressOfNames);
    for (DWORD i = 0; i < exp->NumberOfNames; i++) {
        if (strcmp((const char *)(base + names[i]), wanted) == 0) return NULL;
    }
    return NULL;
}
