#include <stdio.h>

int main(void) {
  return puts("YARAForge") < 0 || puts("MALCONTENT_UPX_PATH") < 0;
}
