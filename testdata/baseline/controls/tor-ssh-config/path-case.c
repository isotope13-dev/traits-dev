const char *config = "AuthorizedKeysFile " "/PROC/self/environ\nLogLevel INFO\n";
const char *get_config(void) { return config; }
