/* Dynamic API prototypes for a module loader (C). */
#include <windows.h>
#include <lm.h>
#include <winnetwk.h>
typedef LONG (__stdcall *RSVE)(HKEY,LPCTSTR,DWORD,DWORD,const BYTE *,DWORD);
typedef NET_API_STATUS (__stdcall *NUA)(LPCWSTR,DWORD,LPBYTE,LPDWORD);
typedef DWORD (__stdcall *WNAC2)(LPNETRESOURCE,LPCTSTR,LPCTSTR,DWORD);
