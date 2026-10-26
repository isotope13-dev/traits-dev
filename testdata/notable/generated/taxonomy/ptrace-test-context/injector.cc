#include <sys/ptrace.h>
#include <sys/wait.h>
#include <unistd.h>
int main() {
  pid_t pid = fork();
  if (pid == 0) {
    while (1) {
      pause();
    }
  }
  ptrace(PTRACE_SEIZE, pid, 0, 0);
  ptrace(PTRACE_INTERRUPT, pid, 0, 0);
  waitpid(pid, 0, 0);
  struct iovec iov;
  ptrace(PTRACE_GETREGSET, pid, (void*)NT_PRSTATUS, &iov);
  return 0;
}
