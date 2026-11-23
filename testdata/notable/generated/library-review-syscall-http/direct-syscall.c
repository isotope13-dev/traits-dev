long run(char *path, char **argv) { return syscall(59, path, argv, 0); }
