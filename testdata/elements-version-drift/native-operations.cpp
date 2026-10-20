void operations() {
    const char *alphabet = "0123456789abcdef";
    for (int i = 0; i < 16; ++i)
        data[i] ^= mask[i];
    GetProcAddress(module, "CryptGenRandom");
}
const char *opcode = "OP_RETURN";
const char *representation = "scriptPubKey hex";
