#include <unistd.h>
int main(int argc, char **argv) { return argc > 1 ? unlink(argv[1]) : 0; }
