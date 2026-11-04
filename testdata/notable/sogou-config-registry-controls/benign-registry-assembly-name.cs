using System.Reflection;
using Microsoft.Win32;
class NameResolver {
 static object Load() {
   return Assembly.Load((string)Registry.GetValue(@"HKEY_CURRENT_USER\Software\Example", "name", null));
 }
}
