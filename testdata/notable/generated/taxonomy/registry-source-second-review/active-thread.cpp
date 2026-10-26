void run(HANDLE t) { SuspendThread(t); GetThreadContext(t, &ctx); SetThreadContext(t, &ctx); ResumeThread(t); }
