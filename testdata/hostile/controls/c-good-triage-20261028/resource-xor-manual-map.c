// Synthetic hostile control: XOR-decodes a bundled resource and maps the
// result as a PE image. Exercises source-pe-resource-access together with
// its source-resource-manual-pe-map and source-resource-xor-manual-map
// consumers after the neutral rename.
#include <windows.h>
#include <string.h>

void *map_bundled_image(HMODULE carrier) {
    HRSRC res = FindResourceW(carrier, MAKEINTRESOURCEW(101), RT_RCDATA);
    HGLOBAL handle = LoadResource(carrier, res);
    unsigned char *blob = (unsigned char *)LockResource(handle);
    DWORD total = SizeofResource(carrier, res);
    for (DWORD i = 0; i < total; i++) {
        blob[i] ^= 0x5A;
    }
    PIMAGE_NT_HEADERS nt = (PIMAGE_NT_HEADERS)(blob +
        ((PIMAGE_DOS_HEADER)blob)->e_lfanew);
    DWORD entry = nt->OptionalHeader.AddressOfEntryPoint;
    DWORD imagesz = nt->OptionalHeader.SizeOfImage;
    DWORD sections = nt->FileHeader.NumberOfSections;
    void *base = VirtualAlloc(NULL, imagesz, MEM_COMMIT | MEM_RESERVE,
                              PAGE_READWRITE);
    memcpy(base, blob, total);
    DWORD oldProt = 0;
    VirtualProtect(base, entry, 64, PAGE_EXECUTE_READ, &oldProt);
    (void)sections;
    return base;
}
