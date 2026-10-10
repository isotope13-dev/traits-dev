void put(int pid, void *local, void *remote) { process_vm_writev(pid, local, 1, remote, 1, 0); }
