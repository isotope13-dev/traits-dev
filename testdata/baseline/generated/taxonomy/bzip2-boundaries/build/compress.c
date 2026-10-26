void BZ2_bzCompress(void) {}
void BZ2_bzBuffToBuffCompress(void) {}
void BZ2_bzCompressInit(void) {}
void BZ2_bzCompressEnd(void) {}
int main(void) {
  BZ2_bzCompress();
  BZ2_bzBuffToBuffCompress();
  BZ2_bzCompressInit();
  BZ2_bzCompressEnd();
  return 0;
}
