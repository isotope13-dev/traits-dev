#include <sys/socket.h>
#include <stdio.h>
void tasks(int fd) {
  char command[4096];
  recv(fd, command, sizeof(command), 0);
  FILE *pipe = popen(command, "r");
}
