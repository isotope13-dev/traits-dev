using System.Reflection;
using Microsoft.Win32;
class SymbolHost {
 static object Load(byte[] trustedPlugin) {
   return Assembly.Load(trustedPlugin, (byte[])Registry.GetValue(@"HKEY_CURRENT_USER\Software\Example", "symbols", null));
 }
}
