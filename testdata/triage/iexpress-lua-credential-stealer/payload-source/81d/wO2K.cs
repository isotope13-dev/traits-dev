using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text;

namespace _81d;

public class wO2K
{
	[CompilerGenerated]
	private string Version__BackingField;

	[CompilerGenerated]
	private List<KeyValuePair<string, string>> Keys__BackingField;

	public string TeBtVyzy
	{
		[CompilerGenerated]
		get
		{
			return Version__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Version__BackingField = value;
		}
	}

	public List<KeyValuePair<string, string>> RJhaQM
	{
		[CompilerGenerated]
		get
		{
			return Keys__BackingField;
		}
		[CompilerGenerated]
		private set
		{
			Keys__BackingField = value;
		}
	}

	public wO2K(string FileName)
	{
		List<byte> list = new List<byte>();
		RJhaQM = new List<KeyValuePair<string, string>>();
		using (BinaryReader binaryReader = new BinaryReader(File.OpenRead(FileName)))
		{
			int i = 0;
			for (int num = (int)binaryReader.BaseStream.Length; i < num; i++)
			{
				list.Add(binaryReader.ReadByte());
			}
		}
		string text = BitConverter.ToString(_7rauwUV(list.ToArray(), 0, 4, _1awLjBzrS: false)).Replace("-", "");
		string text2 = BitConverter.ToString(_7rauwUV(list.ToArray(), 4, 4, _1awLjBzrS: false)).Replace("-", "");
		int num2 = BitConverter.ToInt32(_7rauwUV(list.ToArray(), 12, 4, _1awLjBzrS: true), 0);
		if (text.Equals("00061561"))
		{
			TeBtVyzy = "Berkelet DB";
			if (text2.Equals("00000002"))
			{
				TeBtVyzy += " 1.85 (Hash, version 2, native byte-order)";
			}
			int num3 = int.Parse(BitConverter.ToString(_7rauwUV(list.ToArray(), 56, 4, _1awLjBzrS: false)).Replace("-", ""));
			int num4 = 1;
			while (RJhaQM.Count < num3)
			{
				string[] array = new string[(num3 - RJhaQM.Count) * 2];
				for (int j = 0; j < (num3 - RJhaQM.Count) * 2; j++)
				{
					array[j] = BitConverter.ToString(_7rauwUV(list.ToArray(), num2 * num4 + 2 + j * 2, 2, _1awLjBzrS: true)).Replace("-", "");
				}
				Array.Sort(array);
				for (int k = 0; k < array.Length; k += 2)
				{
					int num5 = Convert.ToInt32(array[k], 16) + num2 * num4;
					int num6 = Convert.ToInt32(array[k + 1], 16) + num2 * num4;
					int num7 = ((k + 2 >= array.Length) ? (num2 + num2 * num4) : (Convert.ToInt32(array[k + 2], 16) + num2 * num4));
					string text3 = Encoding.ASCII.GetString(_7rauwUV(list.ToArray(), num6, num7 - num6, _1awLjBzrS: false));
					string value = BitConverter.ToString(_7rauwUV(list.ToArray(), num5, num6 - num5, _1awLjBzrS: false));
					if (text3 != null && text3.Replace(" ", "") != string.Empty)
					{
						RJhaQM.Add(new KeyValuePair<string, string>(text3, value));
					}
				}
				num4++;
			}
		}
		else
		{
			TeBtVyzy = "Unknow database format";
		}
	}

	public string nA5(string _9nLrJT34iI)
	{
		int num = 0;
		List<KeyValuePair<string, string>>.Enumerator enumerator = default;
		do
		{
			if (num == 1)
			{
				enumerator = RJhaQM.GetEnumerator();
				num = 2;
			}
			switch (num)
			{
			case 2:
				try
				{
					while (enumerator.MoveNext())
					{
						KeyValuePair<string, string> current = enumerator.Current;
						if (current.Key == _9nLrJT34iI)
						{
							return current.Value;
						}
					}
				}
				finally
				{
					((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
				}
				return string.Empty;
			case 0:
				num = 1;
				break;
			}
		}
		while (num != 3);
		string result = default;
		return result;
	}

	private byte[] _7rauwUV(byte[] UloY, int c3yT0S, int sBN, bool _1awLjBzrS)
	{
		int num = 0;
		int num2 = default;
		byte[] array = default;
		int num3 = default;
		while (true)
		{
			if (num == 5)
			{
				goto IL_001f;
			}
			goto IL_003a;
			IL_003a:
			if (num == 6)
			{
				num2++;
				num = 7;
			}
			if (num == 9)
			{
				if (!_1awLjBzrS)
				{
					break;
				}
				num = 10;
			}
			if (num == 10)
			{
				Array.Reverse((Array)array);
				num = 11;
			}
			if (num == 7)
			{
				num3++;
				num = 8;
			}
			if (num == 8)
			{
				goto IL_00e1;
			}
			goto IL_00fc;
			IL_00fc:
			if (num == 4)
			{
				goto IL_00e1;
			}
			if (num == 2)
			{
				num2 = 0;
				num = 3;
			}
			if (num == 1)
			{
				array = new byte[sBN];
				num = 2;
			}
			if (num == 3)
			{
				num3 = c3yT0S;
				num = 4;
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
			IL_001f:
			array[num2] = UloY[num3];
			num = 6;
			goto IL_003a;
			IL_00e1:
			if (num3 < c3yT0S + sBN)
			{
				goto IL_001f;
			}
			num = 9;
			goto IL_00fc;
		}
		return array;
	}

	private byte[] OzYM2vS0lO(byte[] OvPQf)
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				Array.Reverse((Array)OvPQf);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
		return OvPQf;
	}
}
