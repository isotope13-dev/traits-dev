/* Independent, ordinary dynamic TLS and symbol lookup operations. */
extern void *__tls_get_addr(void *);
extern void *dlsym(void *, const char *);
char initialized_data[110000] = {1};
const char *version(void) { return "test"; }
void *lookup(void *index) { return __tls_get_addr(index); }
void *lookup_symbol(void *handle, const char *name) { return dlsym(handle, name); }
