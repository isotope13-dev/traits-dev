int read_kernel_memory(void) {
    return open("/dev/kmem", 0);
}
