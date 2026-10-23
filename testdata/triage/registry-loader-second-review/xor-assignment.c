void transform(unsigned char *a, unsigned char *b, unsigned i, unsigned n) { a[i] ^= b[i % n]; }
