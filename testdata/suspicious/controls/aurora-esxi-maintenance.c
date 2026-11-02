/* Benign control: ESXi maintenance utility. Stops one operator-named hung
 * guest, installs a legal login banner, and records datastore contents.
 * No file encryption, no key wrapping, no extortion text. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void stop_hung_guest(const char *world_id)
{
    char cmd[160];
    snprintf(cmd, sizeof cmd,
             "esxcli vm process kill --type=soft --world-id=%s", world_id);
    if (system(cmd) != 0)
        fprintf(stderr, "soft stop failed for %s; ask the VM owner\n", world_id);
}

static void list_guests(void)
{
    system("esxcli vm process list");
}

static void install_legal_banner(void)
{
    FILE *f = fopen("/etc/ssh/sshd-banner", "w");
    char cfg[4096];
    FILE *c;
    if (!f) return;
    fputs("Authorized use only. Activity on this system is logged.\n", f);
    fclose(f);
    c = fopen("/etc/ssh/sshd_config", "r");
    if (c) {
        size_t n = fread(cfg, 1, sizeof cfg - 1, c);
        fclose(c);
        cfg[n] = 0;
        if (!strstr(cfg, "Banner")) {
            FILE *a = fopen("/etc/ssh/sshd_config", "a");
            if (a) { fputs("\nBanner /etc/ssh/sshd-banner\n", a); fclose(a); }
        }
    }
}

int main(int argc, char **argv)
{
    list_guests();
    if (argc > 1) stop_hung_guest(argv[1]);
    install_legal_banner();
    return 0;
}
