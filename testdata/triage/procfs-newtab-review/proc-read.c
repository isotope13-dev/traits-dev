#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
void inspect(int pid, char *buf) {
  char path[64];
  snprintf(path, sizeof(path), "/proc/%d/mem", pid);
  int fd = open(path, O_RDONLY);
  read(fd, buf, 4);
  close(fd);
}
