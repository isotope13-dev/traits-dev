/* Compile to ELF so the binary-only Go decoder matcher is in scope. */
#include <stdio.h>
static const char decoder_method[] = "compress/zstd.(*Decoder)";
int main(void) { return puts(decoder_method) < 0; }
