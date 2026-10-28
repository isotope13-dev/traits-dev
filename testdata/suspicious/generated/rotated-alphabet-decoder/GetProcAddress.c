#include <stddef.h>
#include <stdint.h>
static const uint8_t symbols[64] = {0x37, 0x21, 0x7d, 0x57, 0x34, 0x77, 0x30, 0x6a, 0x75, 0x36, 0x43, 0x3c, 0x6c, 0x62, 0x69, 0x76, 0x72, 0x5e, 0x5a, 0x65, 0x6d, 0x23, 0x2d, 0x63, 0x45, 0x3a, 0x35, 0x73, 0x48, 0x64, 0x24, 0x49, 0x38, 0x2a, 0x39, 0x40, 0x4a, 0x78, 0x51, 0x44, 0x7a, 0x52, 0x66, 0x4c, 0x70, 0x7e, 0x5f, 0x41, 0x29, 0x67, 0x3b, 0x68, 0x55, 0x46, 0x3f, 0x2e, 0x47, 0x5b, 0x4e, 0x6f, 0x50, 0x58, 0x7b, 0x71};
static const char *reveal(const char *text, size_t salt, size_t size) {
    static char output[256];
    uint8_t ring[64];
    for (size_t cursor = 0; cursor < 64; ++cursor) {
        ring[cursor] = symbols[(cursor + salt) % 64];
    }
    size_t pos = 0;
    for (size_t block = 0; pos < size; block += 4) {
        uint8_t q[4] = {0};
        for (size_t j = 0; j < 4; ++j) {
            for (size_t n = 0; n < 64; ++n) {
                if (ring[n] == text[block+j]) { q[j] = n; break; }
            }
        }
        uint8_t a = q[0], b = q[1], c = q[2], d = q[3];
        output[pos++] = (a << 2) | (b >> 4);
        if (pos < size) output[pos++] = (b << 4) | (c >> 2);
        if (pos < size) output[pos++] = (c << 6) | d;
    }
    output[pos] = 0;
    return output;
}
void *resolve(void *module) {
    return GetProcAddress(module, reveal("vUe;eJofsmh@rm.J:FjL-#vD:U.#trailing-noise", 62, 21));
}
