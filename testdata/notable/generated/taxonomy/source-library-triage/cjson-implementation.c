/* Minimal implementation-symbol fixture; not a runnable cJSON replacement. */
const char *cJSON_Version(void) { return "1.7.17"; }
void cJSON_InitHooks(void *hooks) { (void)hooks; }
void *cJSON_ParseWithOpts(const char *s, const char **end, int strict) {
    (void)s; (void)end; (void)strict; return 0;
}
char *cJSON_PrintUnformatted(const void *item) { (void)item; return 0; }
