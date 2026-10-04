void inspect(unsigned long *free_bytes, unsigned long *total) { cudaMemGetInfo(free_bytes, total); }
