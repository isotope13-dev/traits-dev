#include <windows.h>
void invoke(void *context) {
    CallEnclave((LPENCLAVE_ROUTINE)RtlCaptureContext, context, FALSE, nullptr);
    CallEnclave((LPENCLAVE_ROUTINE)NtContinue, context, FALSE, nullptr);
}
void timestamps(void *request) {
    CallEnclave((LPENCLAVE_ROUTINE)SetCcTimeStamps, request, FALSE, nullptr);
}
