// Inert static-analysis fixture; do not execute. Prototypes are scaffolding.
extern void uncompress(void);
extern void RtlDecompressBuffer(void);
extern void aP_depack_safe(void);
void transform(void) { uncompress(); RtlDecompressBuffer(); aP_depack_safe(); __asm__("call bp_decompress"); }
