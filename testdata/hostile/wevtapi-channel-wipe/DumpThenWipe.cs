using System;
using System.Runtime.InteropServices;
using System.Text;

static class Native
{
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern IntPtr EvtOpenChannelEnum(IntPtr session, int flags);
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern bool EvtNextChannelPath(IntPtr channelEnum, int size, StringBuilder buffer, out int used);
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern bool EvtClearLog(IntPtr session, string path, string target, int flags);
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern IntPtr EvtQuery(IntPtr session, string path, string query, int flags);
    [DllImport("wevtapi.dll", SetLastError = true)] public static extern bool EvtRender(IntPtr ctx, IntPtr evt, int flags, int size, StringBuilder buf, out int used, out int count);
}

class Program
{
    static void Main()
    {
        IntPtr e = Native.EvtOpenChannelEnum(IntPtr.Zero, 0);
        var sb = new StringBuilder(512);
        int used;
        while (Native.EvtNextChannelPath(e, sb.Capacity, sb, out used))
        {
            string chan = sb.ToString();
            Native.EvtClearLog(IntPtr.Zero, chan, null, 0);
        }
    }
}
