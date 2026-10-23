$source = @"
[DllImport("secur32.dll")] public static extern int AddSecurityPackage(string name, IntPtr options);
"@
