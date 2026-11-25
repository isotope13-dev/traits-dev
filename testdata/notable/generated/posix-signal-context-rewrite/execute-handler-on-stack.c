#include <sys/ucontext.h>

void ExecuteHandlerOnCustomStack(int code, siginfo_t *siginfo, void *context, size_t customSp) {
    CONTEXT context2;
    RtlCaptureContext(&context2);
    context2.Rsp = (size_t)customSp;
    context2.Rip = (size_t)signal_handler_worker;
    RtlRestoreContext(&context2, NULL);
}
