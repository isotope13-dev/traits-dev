void worker(){
HANDLE token; OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY|TOKEN_DUPLICATE, &token);
DuplicateToken(token, SecurityImpersonation, &copy);
HANDLE thread=CreateThread(0,0,callback,0,CREATE_SUSPENDED,0);
ZwSetInformationThread(thread, ThreadHideFromDebugger, 0, 0);
ZwSetInformationThread(thread, ThreadImpersonationToken, &copy, sizeof(copy));
NtResumeThread(thread,0);
}
