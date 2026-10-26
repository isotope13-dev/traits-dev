#include <sys/module.h>
#include <sys/linker.h>
int handler(SYSCTL_HANDLER_ARGS) { int mib = KERN_PROC_PID; return 0; }
