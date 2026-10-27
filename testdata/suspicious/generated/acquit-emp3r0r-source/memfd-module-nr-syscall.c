int f(void *image) { int fd = memfd_create("module", 0); return syscall(__NR_finit_module, fd, "", 0); }
