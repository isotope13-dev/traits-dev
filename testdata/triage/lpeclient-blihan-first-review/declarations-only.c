extern void gost28147_encrypt(void);
extern void aes_cbc_decrypt(void);
extern void threefish_decrypt(void);
extern int HeapPageAllocator_ProtectPages(void *, unsigned long, unsigned long);
const char *notes = "crypto.aes_cbc_decrypt(data, key)";
