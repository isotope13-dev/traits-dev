using System.Security.Cryptography.X509Certificates;
using Microsoft.Win32;
using System.Reflection;
class Configuration {
    static bool Compare(X509Certificate a, X509Certificate b) {
        return a.Equals(b);
    }
    static object Read() {
        return Registry.GetValue(@"HKEY_CURRENT_USER\Software\Example", "Configuration", null);
    }
    static Assembly Load(byte[] bytes) {
        return Assembly.Load(bytes);
    }
}
