#include <sys/ptrace.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
void modify(int pid, unsigned long addr, const char *buf) {
  char path[64];
  ptrace(PTRACE_SEIZE, pid, 0, 0);
  snprintf(path, sizeof(path), "/proc/%d/mem", pid);
  int fd = open(path, O_RDWR);
  lseek(fd, addr, SEEK_SET);
  write(fd, buf, 4);
  close(fd);
}
