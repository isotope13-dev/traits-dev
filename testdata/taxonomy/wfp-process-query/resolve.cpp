#include <fwpmu.h>
void resolve(WCHAR* path) {
    FWP_BYTE_BLOB* id = nullptr;
    FwpmGetAppIdFromFileName0(path, &id);
    FwpmFreeMemory0(reinterpret_cast<void**>(&id));
}
