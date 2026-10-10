void get(int pid, void *local, void *remote) { process_vm_readv(pid, local, 1, remote, 1, 0); }
