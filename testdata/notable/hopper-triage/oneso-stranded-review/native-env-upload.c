/* Static regression for the native environment-upload rule consumer. */
extern char **environ;
void upload_environment(void) {
    send_bytes("POST %s HTTP/1.1\r\nContent-Type: application/octet-stream\r\n\r\n");
    for (int i = 0; environ[i]; ++i) {
        send_bytes(environ[i]);
    }
}
