int IsDebuggerPresent(void); void Log(int);
void wait(void) { if (IsDebuggerPresent()) Log(1); while (1) {} }
