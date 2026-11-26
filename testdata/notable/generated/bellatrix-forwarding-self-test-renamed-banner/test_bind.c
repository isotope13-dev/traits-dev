/*
 * project -- forwarding self-test.
 *
 * Calls the real bind_real and checks the seven trampoline destinations.
 * This is the test the path bug slipped past: a bind_real that resolves
 * nothing looks identical to one that works from the outside, because the
 * trampolines return zero either way. All seven pointers being NULL is
 * exactly the failure mode that went unnoticed.
 *
 * Including proxy.c gives access to the static function and the globals
 * without widening the production API.
 *
 * Not part of `make test` alone -- run it as `make check-bind`.
 */
#include <windows.h>
#include <stdio.h>

#include "../src/proxy.c"

static int check(const char *what, void *got)
{
    int ok = (got != NULL);
    printf("  %-32s %p  %s\n", what, got, ok ? "ok" : "NULL");
    return ok ? 0 : 1;
}

int main(void)
{
    bx_context ctx;
    int bad = 0;

    ctx.peb = (bx_peb *)NtCurrentTeb()->ProcessEnvironmentBlock;
    ctx.blob_base = 0;
    ctx.blob_size = 0;
    ctx.kernel32 = 0;
    ctx.user32 = 0;
    ctx.load_library_a = 0;
    ctx.get_proc_address = 0;
    ctx.last_status = 0;

    if (bx_resolve_all(&ctx) != BX_OK) {
        printf("bx_resolve_all failed (status=%u)\n", ctx.last_status);
        return 1;
    }

    bind_real(&ctx);

    bad |= check("CorCreateNGenProcess",    bx_real_cor_create_ngen_process);
    bad |= check("CorGetNGenPolicy",        bx_real_cor_get_ngen_policy);
    bad |= check("CorGetSvc",               bx_real_cor_get_svc);
    bad |= check("CorInitSvcLogger",        bx_real_cor_init_svc_logger);
    bad |= check("CorSetCriticalTaskState", bx_real_cor_set_critical_task_state);
    bad |= check("CorStopNonCriticalTask",  bx_real_cor_stop_non_critical_task);
    bad |= check("CorSvcLog",               bx_real_cor_svc_log);

    printf(bad ? "\nFAIL: forwarding unresolved\n"
               : "\nall seven trampoline targets resolved\n");
    return bad;
}
