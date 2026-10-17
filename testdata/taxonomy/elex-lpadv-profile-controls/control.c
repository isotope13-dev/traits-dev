#pragma section(".data", read, write)
__declspec(allocate(".data")) char markers[] =
"CShareMemory_\0LPMAPSTIC\0LPSYNCSTIC\0Local\\\0Global\\\0SM10\0"
"function fnOnError(msg,url,lineno){return true;}window.onerror=fnOnError;\0JavaScript\0"
"{8856F961-340A-11D0-A96B-00C04FD705A2}\0CWebBrowser2\0"
".ini\0OPEN\0http://example.test/\0SECURITY_WORLD_SID_AUTHORITY\0GENERIC_ALL\0"
"SECURITY_WORLD_SID_AUTHORITY\0GENERIC_ALL\0"
"AfxEnableControlContainer\0AfxSocketInit\0MFC42.DLL\0getenv\0"
"ShellExecuteA\0CreateFileMappingA\0MapViewOfFile\0CreateMutexA\0"
"SetEntriesInAclA\0InitializeSecurityDescriptor\0SetNamedSecurityInfoW\0"
"SetSecurityDescriptorDacl\0InitializeAcl\0MakeAbsoluteSD\0"
"SystemParametersInfoA\0AfxWinMain\0";
__declspec(dllimport) void AfxWinMain(void);
__declspec(dllimport) void CreateMutexA(void);
__declspec(dllimport) void GetModuleFileNameA(void);
__declspec(dllimport) void GetModuleHandleA(void);
__declspec(dllimport) void SetSecurityDescriptorDacl(void);
__declspec(dllimport) void InitializeAcl(void);
__declspec(dllimport) void AddAce(void);
__declspec(dllimport) void GetAclInformation(void);
__declspec(dllimport) void MakeAbsoluteSD(void);
__declspec(dllimport) void ShellExecuteA(void);
__declspec(dllimport) void SetEntriesInAclA(void);
__declspec(dllimport) void InitializeSecurityDescriptor(void);
__declspec(dllimport) void SetNamedSecurityInfoW(void);
__declspec(dllimport) void CreateFileMappingA(void);
__declspec(dllimport) void AfxEnableControlContainer(void);
__declspec(dllimport) void AfxSocketInit(void);
__declspec(allocate(".rdata")) void *refs[] = {AfxWinMain, CreateMutexA, ShellExecuteA, SetEntriesInAclA, InitializeSecurityDescriptor, SetNamedSecurityInfoW, CreateFileMappingA, AfxEnableControlContainer, AfxSocketInit, GetModuleFileNameA, GetModuleHandleA, SetSecurityDescriptorDacl, InitializeAcl, AddAce, GetAclInformation, MakeAbsoluteSD};
void mainCRTStartup(void) { (void)markers; (void)refs; }
