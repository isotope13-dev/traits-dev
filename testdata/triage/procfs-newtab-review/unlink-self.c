#include <unistd.h>
int main(int argc, char **argv) { return unlink(argv[0]); }
