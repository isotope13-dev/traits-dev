#include <stdint.h>
#include <stddef.h>

typedef struct {
    uint32_t AddressOfFunctions;
    uint32_t AddressOfNames;
    uint32_t AddressOfNameOrdinals;
    uint32_t NumberOfNames;
} EXPORT_DIR_VIEW;

uint32_t hash_symbol_name(const char *name) {
    uint32_t h = 0x811c9dc5u;
    while (name && *name) {
        h = (h ^ (uint8_t)*name) * 0x01000193u;
        name++;
    }
    return h;
}

int inspect_pe_export_table(const uint8_t *image,
                            const EXPORT_DIR_VIEW *dir,
                            uint32_t exp_rva,
                            uint32_t exp_size,
                            uint32_t idx) {
    if (!image || !dir || idx >= dir->NumberOfNames)
        return -1;
    uint32_t rva = dir->AddressOfFunctions;
    if (rva >= exp_rva && rva - exp_rva < exp_size)
        return 1;
    (void)dir->AddressOfNames;
    (void)dir->AddressOfNameOrdinals;
    return 0;
}
