#include <sys/stat.h>
#include <unistd.h>
int main(void) {
  struct stat st;
  if (stat("/proc/self/exe", &st)) return 1;
  if (st.st_mode & S_ISUID) return 1;
  return execl("/bin/true", "true", (char *)0);
}
