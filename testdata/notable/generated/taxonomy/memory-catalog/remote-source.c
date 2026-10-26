void *allocate_remote(void *process, unsigned long length) { return VirtualAllocEx(process, 0, length, 0x1000, 4); }
