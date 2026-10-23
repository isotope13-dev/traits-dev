#include <windows.h>
#include <stdint.h>
#include <string.h>
typedef void (*module_entry_t)(void);
static void execute_coff_module(uint8_t *object, size_t object_len) {
    IMAGE_FILE_HEADER *header = (IMAGE_FILE_HEADER *)object;
    if (object_len < sizeof(*header) ||
        header->Machine != IMAGE_FILE_MACHINE_AMD64 ||
        header->NumberOfSections == 0 || header->PointerToSymbolTable == 0) {
        return;
    }

    IMAGE_SECTION_HEADER *sections = (IMAGE_SECTION_HEADER *)(header + 1);
    IMAGE_SYMBOL *symbols = (IMAGE_SYMBOL *)(object + header->PointerToSymbolTable);
    uint8_t *mapped = VirtualAlloc(NULL, object_len, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!mapped) return;

    for (WORD i = 0; i < header->NumberOfSections; ++i) {
        memcpy(mapped + sections[i].VirtualAddress,
               object + sections[i].PointerToRawData,
               sections[i].SizeOfRawData);
    }
    apply_coff_relocations(mapped, header);
    module_entry_t entry = (module_entry_t)resolve_coff_symbol(
        mapped, symbols, header->NumberOfSymbols, "module_init");
    if (entry) entry();
}


int main(void) { size_t n=0; uint8_t *p=read_user_selected_object(&n); execute_coff_module(p,n); }
