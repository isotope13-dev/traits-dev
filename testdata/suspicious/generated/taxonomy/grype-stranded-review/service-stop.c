#include <signal.h>
#include <stdio.h>
const char *targets[] = {"tomcat", "mysql"};
void stop_target(int pid) { kill(pid, SIGSTOP); printf("Service PID %d stopped", pid); }
