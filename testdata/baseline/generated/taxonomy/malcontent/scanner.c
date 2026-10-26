#include <stdio.h>

int main(void) {
  return puts("github.com/chainguard-dev/malcontent") < 0 ||
         puts("YARAForge") < 0 ||
         puts("MALCONTENT_UPX_PATH") < 0;
}
