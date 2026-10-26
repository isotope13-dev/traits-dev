#include <sys/ptrace.h>
int main(void) {
  return ptrace(PTRACE_TRACEME, 0, 0, 0);
}
