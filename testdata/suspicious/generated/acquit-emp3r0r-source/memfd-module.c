int f(void *image) { int fd = memfd_create("module", 0); return finit_module(fd, "", 0); }
