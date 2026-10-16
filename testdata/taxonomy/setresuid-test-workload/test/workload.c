// Syscall trace workload: each setid variant is an isolated probe in
// its own test function, run as root so the calls are identities.
#include <unistd.h>

#define TEST_CHECK(x) do { if (!(x)) return; } while (0)

void runSetgid(void) {
  TEST_CHECK(setgid(0) == 0);
}

void runSetresuid(void) {
  TEST_CHECK(setresuid(0, 0, 0) == 0);
}

void runSetresgid(void) {
  TEST_CHECK(setresgid(0, 0, 0) == 0);
}

int main(void) {
  runSetgid();
  runSetresuid();
  runSetresgid();
  return 0;
}
