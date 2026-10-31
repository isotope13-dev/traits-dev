#include <windows.h>
#include <wtsapi32.h>
#include <stdio.h>
volatile void *apis[] = {
 (void *)&OpenProcessToken, (void *)&DuplicateTokenEx,
 (void *)&CreateProcessWithTokenW, (void *)&SetThreadToken,
 (void *)&WTSEnumerateProcessesW
};
int main(void) {
 puts("lsass.exe SeDebugPrivilege Failed to impersonate token");
 return apis[0] == NULL;
}
