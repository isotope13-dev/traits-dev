void demo(void *fd, char *buf, int n) {
  PR_Read(fd, buf, n);
  PR_Write(fd, buf, n);
}
