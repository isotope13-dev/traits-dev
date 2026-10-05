#include <openssl/ssl.h>
#include <sys/socket.h>
#include <string.h>

int deliver(SSL *tls, int fd, const char *message) {
    char response[1024];
    recv(fd, response, sizeof(response), 0);
    send(fd, "EHLO mailhost\r\n", 15, 0);
    recv(fd, response, sizeof(response), 0);
    send(fd, "STARTTLS\r\n", 10, 0);
    recv(fd, response, sizeof(response), 0);
    SSL_set_fd(tls, fd);
    if (SSL_connect(tls) != 1) return -1;
    SSL_write(tls, "MAIL FROM:<sender@example.test>\r\n", 33);
    SSL_read(tls, response, sizeof(response));
    SSL_write(tls, "RCPT TO:<recipient@example.test>\r\n", 34);
    SSL_read(tls, response, sizeof(response));
    SSL_write(tls, "DATA\r\n", 6);
    SSL_read(tls, response, sizeof(response));
    SSL_write(tls, message, strlen(message));
    SSL_write(tls, "\r\n.\r\n", 5);
    return SSL_read(tls, response, sizeof(response));
}
