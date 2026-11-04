using System.Reflection;
using Microsoft.Win32;
class Selector {
 static object Load(byte[] trustedPlugin) {
   return Assembly.Load(Choose(trustedPlugin, (byte[])Registry.GetValue(@"HKEY_CURRENT_USER\Software\Example", "theme", null)));
 }
 static byte[] Choose(byte[] plugin, byte[] theme) { return plugin; }
}
