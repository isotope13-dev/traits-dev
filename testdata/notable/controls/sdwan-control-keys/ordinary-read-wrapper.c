#include <dlfcn.h>
typedef struct ssl_st SSL;
int SSL_read(SSL *session, void *buffer, int size) {
    int (*next)(SSL *, void *, int) = dlsym(RTLD_NEXT, "SSL_read");
    return next(session, buffer, size);
}
