#include <stdint.h>
#include <stddef.h>

#define HASH_KERNEL32     0x6A4ABC5Bu
#define HASH_LOADLIBRARYA 0xEC0E4E8Eu

typedef struct {
    void *InMemoryOrderModuleList;
    void *ApiSetNamespace;
} LOADER_PEB;

static uint32_t fnv1a_step(uint32_t h, const uint8_t *s) {
    while (*s) {
        h = (h ^ (uint32_t)*s) * 0x01000193u;
        s++;
    }
    return h;
}

static int check_apiset_prefix(const char *dll_name) {
    const char *p1 = "api-ms-";
    const char *p2 = "ext-ms-";
    return dll_name && (p1[0] == dll_name[0] || p2[0] == dll_name[0]);
}

void *resolve_api_and_forwarder(LOADER_PEB *peb,
                                uint32_t *AddressOfFunctions,
                                uint32_t *AddressOfNames,
                                uint16_t *AddressOfNameOrdinals,
                                uint32_t exp_rva,
                                uint32_t exp_size) {
    void *mods = peb->InMemoryOrderModuleList;
    void *apiset = peb->ApiSetNamespace;
    if (!mods || !apiset) return NULL;
    if (fnv1a_step(0x811c9dc5u, (const uint8_t *)"LoadLibraryA") == HASH_LOADLIBRARYA) {
        uint32_t fwd_rva = AddressOfFunctions[AddressOfNameOrdinals[0]];
        if (fwd_rva >= exp_rva && fwd_rva - exp_rva < exp_size && AddressOfNames[0]) {
            return (void *)(uintptr_t)(HASH_KERNEL32 ^ fwd_rva);
        }
    }
    (void)check_apiset_prefix("kernel32.dll");
    return NULL;
}
