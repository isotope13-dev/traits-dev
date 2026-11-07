#include <windows.h>
#include <winevt.h>
#pragma comment(lib, "wevtapi.lib")

int wmain(void)
{
    WCHAR chan[512];
    DWORD used = 0;
    EVT_HANDLE it = EvtOpenChannelEnum(NULL, 0);
    if (!it)
        return 1;
    while (EvtNextChannelPath(it, ARRAYSIZE(chan), chan, &used)) {
        EvtClearLog(NULL, chan, NULL, 0);
    }
    EvtClose(it);
    return 0;
}
