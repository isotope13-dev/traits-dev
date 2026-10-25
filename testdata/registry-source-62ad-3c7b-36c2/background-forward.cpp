// Ordinary background forwarding of a developer database, using the command
// documented in tailscale/tailcat README. Hiding a console is not C2 tasking.
#include <windows.h>
int main() {
  const char *tool = "tailcat.exe";
  const char *operation = "forward";
  const char *peer = "tcomFwWCCcjS5nKNqAod034nWoJZW0LZqDhhC8U_dKdnDRYQ8uNGFpGQEu";
  STARTUPINFOA si = {sizeof(si)};
  si.wShowWindow = SW_HIDE;
  // Launch plumbing is deliberately omitted; these are the old rule's clues.
  return 0;
}
