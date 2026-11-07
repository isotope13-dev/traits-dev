using System;
using System.Runtime.InteropServices;
using System.Text;

// Interop surface for an event viewer: enumerate channels, read, render,
// export and clear on operator request.
public static class EventLogInterop
{
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern IntPtr EvtOpenChannelEnum(IntPtr session, int flags);
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern bool EvtNextChannelPath(IntPtr channelEnum, int size, StringBuilder buffer, out int used);
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern bool EvtClearLog(IntPtr session, string path, string target, int flags);
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern IntPtr EvtQuery(IntPtr session, string path, string query, int flags);
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern bool EvtNext(IntPtr rs, int n, IntPtr[] events, int timeout, int flags, out int returned);
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern bool EvtRender(IntPtr ctx, IntPtr evt, int flags, int size, StringBuilder buf, out int used, out int count);
}
