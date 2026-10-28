void compress(unsigned char *src, unsigned char *dst, void *workspace) {
    unsigned long used;
    RtlCompressBuffer(0x4, src, 1024, dst, 4096, 4096, &used, workspace);
}
