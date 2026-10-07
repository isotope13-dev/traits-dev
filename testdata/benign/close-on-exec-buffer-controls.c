/* Descriptor hygiene, not dispatch: close-on-exec setter on a buffer. */
#include <fcntl.h>
#define SET_CLOSE_ON_EXEC(fd) fcntl(fd, F_SETFD, FD_CLOEXEC)
void setup(void) {
  SET_CLOSE_ON_EXEC (default_buffered_input);
}
