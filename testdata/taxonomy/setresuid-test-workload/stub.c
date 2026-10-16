// Setuid stub: the group and user root requests are one escalation
// sequence in a single function, outside any test tree.
#include <unistd.h>

int main(void) {
  setresgid(0, 0, 0);
  setresuid(0, 0, 0);
  return 0;
}
