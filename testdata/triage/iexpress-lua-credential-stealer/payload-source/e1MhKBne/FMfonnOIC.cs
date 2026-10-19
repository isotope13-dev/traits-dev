using System;
using System.Runtime.InteropServices;

namespace e1MhKBne;

public static class FMfonnOIC
{
	[DllImport("ntdll.dll", SetLastError = true)]
	public static extern SoEk2Z NtQueryObject([In] IntPtr Handle, [In] TiOT49te ObjectInformationClass, [Out] IntPtr ObjectInformation, [In] int ObjectInformationLength, out int ReturnLength);

	[DllImport("ntdll.dll")]
	internal static extern SoEk2Z NtQuerySystemInformation([In] DPeTMrxslx SystemInformationClass, [In] IntPtr SystemInformation, [In] int SystemInformationLength, out int ReturnLength);
}
