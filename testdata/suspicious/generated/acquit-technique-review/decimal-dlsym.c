#include <stddef.h>
#include <stdint.h>
static const uint8_t symbols[64] = {55, 33, 125, 87, 52, 119, 48, 106, 117, 54, 67, 60, 108, 98, 105, 118, 114, 94, 90, 101, 109, 35, 45, 99, 69, 58, 53, 115, 72, 100, 36, 73, 56, 42, 57, 64, 74, 120, 81, 68, 122, 82, 102, 76, 112, 126, 95, 65, 41, 103, 59, 104, 85, 70, 63, 46, 71, 91, 78, 111, 80, 88, 123, 113};
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
    return dlsym(module, reveal("vUe;eJofsmh@rm.J:FjL-#vD:U.#trailing-noise", 62, 21));
}
