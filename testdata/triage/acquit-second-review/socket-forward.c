#include <sys/socket.h>
void relay(int left, int right) {
  char buffer[4096];
  recv(left, buffer, sizeof(buffer), 0);
  send(right, buffer, sizeof(buffer), 0);
}
