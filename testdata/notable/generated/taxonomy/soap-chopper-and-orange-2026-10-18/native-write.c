void save(void *h, void *buf, unsigned *written) {
 WriteFile(h, buf, 10, written, 0);
}
