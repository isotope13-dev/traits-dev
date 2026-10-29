int IsDebuggerPresent(void); void Sleep(int);
void wait(void) { while (!IsDebuggerPresent()) Sleep(500); while (1) { Sleep(100); } }
