using System.Reflection;
using Microsoft.Win32;
class PluginHost {
  static object Load(byte[] trustedPlugin) {
    var setting = Registry.GetValue(@"HKEY_CURRENT_USER\Software\Example", "theme", null);
    return Assembly.Load(trustedPlugin);
  }
}
