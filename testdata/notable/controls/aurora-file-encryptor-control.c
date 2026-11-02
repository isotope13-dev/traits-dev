/* Benign control: user-invoked hybrid file encryptor for one named file.
 * ChaCha20 content encryption with an RSA-wrapped session key, written to
 * a new output file. No drive sweep, no shadow removal, no in-place
 * destruction of the original. */
#include <stdio.h>
#include <string.h>
#include <openssl/rsa.h>
#include <sodium.h>

int main(int argc, char **argv)
{
    unsigned char k[32], n[12], wrap[512], buf[8192];
    FILE *in, *out;
    RSA *pk = NULL;
    size_t got;
    int wl;
    if (argc != 3) {
        fprintf(stderr, "usage: file_encryptor <input> <output>\n");
        return 2;
    }
    in = fopen(argv[1], "rb");
    out = fopen(argv[2], "wb");
    if (!in || !out) return 1;
    randombytes_buf(k, sizeof k);
    randombytes_buf(n, sizeof n);
    wl = RSA_public_encrypt(32, k, wrap, pk, RSA_PKCS1_OAEP_PADDING);
    if (wl > 0) fwrite(wrap, 1, (size_t)wl, out);
    while ((got = fread(buf, 1, sizeof buf, in)) > 0) {
        crypto_stream_chacha20_ietf_xor(buf, buf, got, n, k);
        fwrite(buf, 1, got, out);
    }
    fclose(in);
    fclose(out);
    return 0;
}
