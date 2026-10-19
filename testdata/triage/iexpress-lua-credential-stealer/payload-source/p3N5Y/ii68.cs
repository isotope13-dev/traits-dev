using System;
using System.Runtime.CompilerServices;

namespace p3N5Y;

public class ii68
{
	[CompilerGenerated]
	private string Application__BackingField;

	[CompilerGenerated]
	private string Username__BackingField;

	[CompilerGenerated]
	private string Password__BackingField;

	[CompilerGenerated]
	private string Host__BackingField;

	public string oVAe
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

	public string S8v
	{
		[CompilerGenerated]
		get
		{
			return Username__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Username__BackingField = value;
		}
	}

	public string _9H5rP7hg2
	{
		[CompilerGenerated]
		get
		{
			return Password__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Password__BackingField = value;
		}
	}

	public string byIdLuuGZbL
	{
		[CompilerGenerated]
		get
		{
			return Host__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Host__BackingField = value;
		}
	}

	public ii68()
	{
		oVAe = "";
		S8v = "";
		_9H5rP7hg2 = "";
		byIdLuuGZbL = "";
	}

	public ii68(string host, string user, string pass, string app)
	{
		byIdLuuGZbL = host;
		S8v = user;
		_9H5rP7hg2 = pass;
		oVAe = app;
	}

	public override string ToString()
	{
		int num = 0;
		string[] array = default;
		do
		{
			if (num == 1)
			{
				array = new string[8];
				num = 2;
			}
			if (num == 4)
			{
				array[2] = "\r\nUsername: ";
				num = 5;
			}
			if (num == 7)
			{
				array[5] = _9H5rP7hg2;
				num = 8;
			}
			if (num == 5)
			{
				array[3] = S8v;
				num = 6;
			}
			if (num == 2)
			{
				array[0] = "Host: ";
				num = 3;
			}
			if (num == 3)
			{
				array[1] = byIdLuuGZbL;
				num = 4;
			}
			if (num == 8)
			{
				array[6] = "\r\nApplication: ";
				num = 9;
			}
			if (num == 6)
			{
				array[4] = "\r\nPassword: ";
				num = 7;
			}
			if (num == 9)
			{
				array[7] = oVAe;
				num = 10;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 10);
		return string.Concat(array);
	}

	public string YK49f1j3()
	{
		int num = 0;
		string[] array = default;
		do
		{
			if (num == 14)
			{
				array[4] = "<br>Password: ";
				num = 15;
			}
			if (num == 3)
			{
				goto IL_0048;
			}
			goto IL_005f;
			IL_011f:
			if (oVAe == null)
			{
				num = 6;
				goto IL_0136;
			}
			goto IL_0262;
			IL_0279:
			if (num == 13)
			{
				array[3] = S8v;
				num = 14;
			}
			if (num == 2)
			{
				S8v = string.Empty;
				num = 3;
			}
			if (num == 18)
			{
				array[8] = "<br><hr>";
				num = 19;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_005f:
			if (num == 15)
			{
				array[5] = _9H5rP7hg2;
				num = 16;
			}
			if (num == 17)
			{
				array[7] = oVAe;
				num = 18;
			}
			if (num == 8)
			{
				byIdLuuGZbL = string.Empty;
				num = 9;
			}
			if (num == 11)
			{
				array[1] = byIdLuuGZbL;
				num = 12;
			}
			if (num == 5)
			{
				goto IL_011f;
			}
			goto IL_0136;
			IL_0136:
			if (num == 16)
			{
				array[6] = "<br>Application: ";
				num = 17;
			}
			if (num == 12)
			{
				array[2] = "<br>Username: ";
				num = 13;
			}
			if (num == 6)
			{
				oVAe = string.Empty;
				num = 7;
			}
			if (num == 1)
			{
				if (S8v != null)
				{
					goto IL_0048;
				}
				num = 2;
			}
			if (num == 9)
			{
				goto IL_01e9;
			}
			goto IL_0200;
			IL_01e9:
			array = new string[9];
			num = 10;
			goto IL_0200;
			IL_0200:
			if (num == 4)
			{
				_9H5rP7hg2 = string.Empty;
				num = 5;
			}
			if (num == 10)
			{
				array[0] = "Host: ";
				num = 11;
			}
			if (num == 7)
			{
				goto IL_0262;
			}
			goto IL_0279;
			IL_0262:
			if (byIdLuuGZbL != null)
			{
				goto IL_01e9;
			}
			num = 8;
			goto IL_0279;
			IL_0048:
			if (_9H5rP7hg2 == null)
			{
				num = 4;
				goto IL_005f;
			}
			goto IL_011f;
		}
		while (num != 19);
		return string.Concat(array);
	}

	public string vk5()
	{
		int num = 0;
		do
		{
			if (num == 8)
			{
				byIdLuuGZbL = string.Empty;
				num = 9;
			}
			if (num == 4)
			{
				_9H5rP7hg2 = string.Empty;
				num = 5;
			}
			if (num == 1)
			{
				if (S8v != null)
				{
					goto IL_0097;
				}
				num = 2;
			}
			if (num == 3)
			{
				goto IL_0097;
			}
			goto IL_00ae;
			IL_0097:
			if (_9H5rP7hg2 == null)
			{
				num = 4;
				goto IL_00ae;
			}
			goto IL_00e7;
			IL_014e:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_00ae:
			if (num == 6)
			{
				oVAe = string.Empty;
				num = 7;
			}
			if (num == 5)
			{
				goto IL_00e7;
			}
			goto IL_00fe;
			IL_0137:
			if (byIdLuuGZbL != null)
			{
				break;
			}
			num = 8;
			goto IL_014e;
			IL_00fe:
			if (num == 2)
			{
				S8v = string.Empty;
				num = 3;
			}
			if (num == 7)
			{
				goto IL_0137;
			}
			goto IL_014e;
			IL_00e7:
			if (oVAe == null)
			{
				num = 6;
				goto IL_00fe;
			}
			goto IL_0137;
		}
		while (num != 9);
		return "[" + string.Join(",", new string[4]
		{
			"\"" + oVAe + "\"",
			"\"" + byIdLuuGZbL + "\"",
			"\"" + Uri.EscapeDataString(S8v) + "\"",
			"\"" + Uri.EscapeDataString(_9H5rP7hg2) + "\""
		}) + "]";
	}
}
