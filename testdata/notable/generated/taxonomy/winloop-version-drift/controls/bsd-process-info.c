int query(int pid) { int mib[] = {CTL_KERN, KERN_PROC, KERN_PROC_PID, pid}; return sysctl(mib, 4, 0, 0, 0, 0); }
