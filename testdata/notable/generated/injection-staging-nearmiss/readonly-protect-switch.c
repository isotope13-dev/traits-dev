// Benign near-miss: VirtualProtect restores PAGE_READONLY while a later,
// unrelated switch statement names PAGE_EXECUTE_READWRITE. The RWX flag
// belongs to the switch label, not to the call, so
// source-rwx-memory-api-call must not fire.
#include <windows.h>

int classify_region(void *base, SIZE_T len, DWORD protect, int *kind) {
    if (protect == PAGE_WRITECOPY) {
        DWORD old = 0;
        if (VirtualProtect(base, len, PAGE_READONLY, &old)) {
            *kind = 1;
            return 1;
        }
        return 0;
    }
    switch (protect) {
    case PAGE_NOACCESS:
        *kind = 0;
        break;
    case PAGE_READONLY:
        *kind = 1;
        break;
    case PAGE_EXECUTE_READWRITE:
        *kind = 7;
        break;
    default:
        *kind = -1;
        break;
    }
    return 1;
}
