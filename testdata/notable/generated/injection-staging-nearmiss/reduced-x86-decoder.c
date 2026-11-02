// Benign near-miss: a crash-dump length decoder that only checks the 0x0F
// two-byte escape. Exercises the neutral decoder atom without the full
// prefix/ModR/M set, so lkm-instruction-decoder must not fire.
int two_byte_escape_len(unsigned char *stream) {
    unsigned char opcode = stream[0];
    unsigned char modrm = stream[1];
    if (opcode == 0x0F) {
        return 2 + ((modrm >> 3) & 1);
    }
    return 1;
}
