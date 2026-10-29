__attribute__((used,noinline)) void marker(void) {
  __asm__ volatile(".byte 0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5");
}
volatile const char provider[] = "libtransport";
int main(void) { return provider[0] == 'x'; }
