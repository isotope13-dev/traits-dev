using System;
using System.Collections.Generic;
using System.IO;

namespace _81d;

public class kKdeGISe : Dictionary<string, Dictionary<string, string>>
{
	public kKdeGISe()
	{
	}

	public kKdeGISe(string filename)
	{
		EKL3d(filename);
	}

	public void EKL3d(string Wl6IZ62P4uL)
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				V34uQaY(File.ReadAllLines(Wl6IZ62P4uL));
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
	}

	public void YzqDO(string _4zyobm)
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				V34uQaY(_4zyobm.Split(new string[1] { Environment.NewLine }, StringSplitOptions.None));
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
	}

	public void fYtt7(string[] vfl)
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				V34uQaY(vfl);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
	}

	private void V34uQaY(string[] hy6o)
	{
		int num = 0;
		int num2 = default;
		string[] array = default;
		string key = default;
		string text = default;
		int num3 = default;
		do
		{
			if (num == 4)
			{
				goto IL_0223;
			}
			if (num == 16)
			{
				goto IL_003e;
			}
			goto IL_0055;
			IL_0223:
			if (num2 >= array.Length)
			{
				num = 18;
				goto IL_023b;
			}
			goto IL_0360;
			IL_0055:
			if (num == 3)
			{
				num2 = 0;
				num = 4;
			}
			if (num == 15)
			{
				base[key][text.Substring(0, num3).TrimEnd(new char[1] { ' ' })] = text.Substring(num3 + 1, text.Length - num3 - 1).TrimEnd(new char[1] { ' ' });
				num = 16;
			}
			if (num == 13)
			{
				if (!text.Contains("="))
				{
					goto IL_003e;
				}
				num = 14;
			}
			if (num == 11)
			{
				goto IL_003e;
			}
			if (num == 10)
			{
				Add(key, new Dictionary<string, string>());
				num = 11;
			}
			if (num == 2)
			{
				array = hy6o;
				num = 3;
			}
			if (num == 1)
			{
				key = string.Empty;
				num = 2;
			}
			if (num == 9)
			{
				if (ContainsKey(key))
				{
					goto IL_003e;
				}
				num = 10;
			}
			if (num == 17)
			{
				goto IL_0223;
			}
			goto IL_023b;
			IL_0279:
			if (text.StartsWith(";"))
			{
				goto IL_003e;
			}
			num = 13;
			goto IL_0295;
			IL_003e:
			num2++;
			num = 17;
			goto IL_0055;
			IL_0360:
			text = array[num2];
			num = 6;
			goto IL_0376;
			IL_0295:
			if (num == 14)
			{
				num3 = text.IndexOf('=');
				num = 15;
			}
			if (num == 8)
			{
				key = text.Substring(1, text.Length - 2).TrimEnd(new char[1] { ' ' });
				num = 9;
			}
			if (num == 7)
			{
				if (!text.EndsWith("]"))
				{
					goto IL_0279;
				}
				num = 8;
			}
			if (num == 5)
			{
				goto IL_0360;
			}
			goto IL_0376;
			IL_0376:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_023b:
			if (num == 6)
			{
				if (!text.StartsWith("["))
				{
					goto IL_0279;
				}
				num = 7;
			}
			if (num == 12)
			{
				goto IL_0279;
			}
			goto IL_0295;
		}
		while (num != 18);
	}
}
