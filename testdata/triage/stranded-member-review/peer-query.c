#include <sys/socket.h>
int query(int descriptor, struct sockaddr *peer, socklen_t *length) {
 return getpeername(descriptor, peer, length);
}
