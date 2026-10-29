int IsDebuggerPresent(void);
void wait(void) { if (IsDebuggerPresent()) { while (1) {} } }
