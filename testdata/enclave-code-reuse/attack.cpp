#include <windows.h>
#include <stdint.h>
// Representative fragments; exports and primitive helpers are resolved by the host.
extern void write64(uintptr_t, uint64_t);
extern void write32(uintptr_t, uint32_t);
extern uintptr_t Initialize, GetCcAttributes, SetCcTimeStamps;
struct Node { uintptr_t object; } node;
struct Request { uint32_t handle; uint64_t controlledQword; } request;
void read_write(uintptr_t source, uintptr_t destination, uint64_t value) {
    node.object = source - 0x2A8;
    CallEnclave((LPENCLAVE_ROUTINE)GetCcAttributes, &request, FALSE, nullptr);
    node.object = destination - 0x2B0;
    write32(destination - 0x29C, 0xC0000510);
    request.controlledQword = value;
    CallEnclave((LPENCLAVE_ROUTINE)SetCcTimeStamps, &request, FALSE, nullptr);
}
void invoke(uintptr_t privateContext, uintptr_t function, uintptr_t capturedStack) {
    CONTEXT state = {};
    CallEnclave((LPENCLAVE_ROUTINE)RtlCaptureContext, &state, FALSE, nullptr);
    state.Rip = function;
    state.Rsp = capturedStack - 8;
    state.Rcx = 0x1234;
    state.Rdx = 0x5678;
    write64(privateContext + offsetof(CONTEXT, Rip), state.Rip);
    write64(privateContext + offsetof(CONTEXT, Rsp), state.Rsp);
    write64(privateContext + offsetof(CONTEXT, Rcx), state.Rcx);
    write64(privateContext + offsetof(CONTEXT, Rdx), state.Rdx);
    CallEnclave((LPENCLAVE_ROUTINE)NtContinue, (void*)privateContext, FALSE, nullptr);
}
