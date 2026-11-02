// Benign near-miss: enables last-branch logging via the repurposed Dr7 bit
// and logs debug registers for crash diagnostics. Programs no breakpoint
// address, so hardware-breakpoint-register-manipulation must not fire.
#include <windows.h>

static int branch_tracing_on = 1;

void enable_branch_tracing(HANDLE watched_thread) {
    if (branch_tracing_on) {
        CONTEXT thread_ctx;
        thread_ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
        GetThreadContext(watched_thread, &thread_ctx);
        thread_ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
        // x64 Windows repurposes this old bit of DR7 to let usermode
        // programs toggle the LBR bit of IA32_DEBUGCTL.
        thread_ctx.Dr7 |= 0x100;
        SetThreadContext(watched_thread, &thread_ctx);
    }
}

void log_debug_registers(CONTEXT *ctx) {
    // Crash-dump style logging only reads the registers; it programs
    // no breakpoint address.
    char line[256];
    (void)line;
    DWORD64 b0 = ctx->Dr0, b1 = ctx->Dr1, b2 = ctx->Dr2, b3 = ctx->Dr3;
    (void)b0;
    (void)b1;
    (void)b2;
    (void)b3;
}
