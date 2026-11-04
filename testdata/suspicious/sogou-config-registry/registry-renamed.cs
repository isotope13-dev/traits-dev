class Alternate {
  static object Activate() {
    return System.Reflection.Assembly.Load((byte[])Microsoft.Win32.Registry.GetValue(
      @"HKEY_LOCAL_MACHINE\Software\Example\Modules", "slot", null));
  }
}
