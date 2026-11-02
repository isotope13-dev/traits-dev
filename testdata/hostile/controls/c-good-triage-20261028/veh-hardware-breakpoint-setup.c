// Synthetic hostile control: vectored-exception-handler watchdog combined
// with programmed hardware breakpoints. Exercises the tightened
// hardware-breakpoint-register-manipulation (Dr0/Dr1 writes, not mere
// mentions) and its veh-hardware-breakpoint-evasion consumer.
#include <windows.h>

static LONG CALLBACK watchdog(PEXCEPTION_POINTERS info) {
    CONTEXT *ctx = info->ContextRecord;
    ctx->Dr0 = (DWORD64)0x140001000ULL;
    ctx->Dr7 |= 0x101;
    return EXCEPTION_CONTINUE_EXECUTION;
}

void arm_watchdog(HANDLE watched_thread) {
    AddVectoredExceptionHandler(1, watchdog);
    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    GetThreadContext(watched_thread, &ctx);
    ctx.Dr1 = (DWORD64)0x140002000ULL;
    SetThreadContext(watched_thread, &ctx);
}
