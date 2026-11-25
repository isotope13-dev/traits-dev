#include <windows.h>

void resume_on_fake_stack(void *target, DWORD64 fake_rsp) {
    CONTEXT ctx;
    RtlCaptureContext(&ctx);
    ctx.Rsp = fake_rsp;
    ctx.Rip = (DWORD64)target;
    RtlRestoreContext(&ctx, NULL);
}
