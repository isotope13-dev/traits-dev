int f(void *image) { int fd = memfd_create("module", 0); return syscall(SYS_finit_module, fd, "", 0); }
