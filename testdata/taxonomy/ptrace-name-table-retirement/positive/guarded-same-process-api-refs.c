#define _GNU_SOURCE
#include <sys/ptrace.h>
#include <sys/uio.h>
#include <unistd.h>

int main(int argc, char **argv) {
  if (argc == 12345) {
    struct iovec local = {argv, sizeof(*argv)};
    struct iovec remote = {argv, sizeof(*argv)};
    ptrace(PTRACE_POKETEXT, getpid(), 0, 0);
    process_vm_writev(getpid(), &local, 1, &remote, 1, 0);
  }
  return 0;
}
