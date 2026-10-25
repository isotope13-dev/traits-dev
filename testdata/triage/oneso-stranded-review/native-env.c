extern char **environ;
void report_environment(void) {
    for (int i = 0; environ[i]; ++i) {
        send_record(environ[i]);
    }
}
