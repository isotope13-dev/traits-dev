using System;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using QUNmAVKTUt;

namespace F3k8m0yephw;

public class k27Ns : T0ipHAo
{
	[CompilerGenerated]
	private string Name__BackingField;

	public override uint HJu9nKBGV4 => 9 + HESCmQXxkE + (uint)Nm7ch.GetBytes().Length;

	public uint HESCmQXxkE => (uint)((rR2w5VYKU.Length + 1) * 2);

	public byte GsJ => 0;

	public string rR2w5VYKU
	{
		[CompilerGenerated]
		get
		{
			return Name__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Name__BackingField = value;
		}
	}

	public k27Ns()
	{
	}

	public k27Ns(string Name, w3F6aB TypedPropertyValue)
	{
		rR2w5VYKU = Name;
		Nm7ch = TypedPropertyValue;
	}

	public override byte[] GetBytes()
	{
		int num = 0;
		byte[] array = default;
		do
		{
			if (num == 1)
			{
				array = new byte[jQzAxt];
				num = 2;
			}
			if (num == 4)
			{
				Buffer.BlockCopy(Encoding.Unicode.GetBytes(rR2w5VYKU), 0, array, 9, 4);
				num = 5;
			}
			if (num == 3)
			{
				Buffer.BlockCopy(BitConverter.GetBytes(HESCmQXxkE), 0, array, 4, 4);
				num = 4;
			}
			if (num == 2)
			{
				Buffer.BlockCopy(BitConverter.GetBytes(jQzAxt), 0, array, 0, 4);
				num = 3;
			}
			if (num == 5)
			{
				Buffer.BlockCopy(Nm7ch.GetBytes(), 0, array, (int)(9 + HESCmQXxkE), Nm7ch.GetBytes().Length);
				num = 6;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 6);
		return array;
	}

	public override string ToString()
	{
		int num = 0;
		StringBuilder stringBuilder = default;
		do
		{
			if (num == 7)
			{
				stringBuilder.AppendFormat("Name: {0}", rR2w5VYKU);
				num = 8;
			}
			if (num == 5)
			{
				stringBuilder.AppendFormat("NameSize: {0} (0x{0:X})", HESCmQXxkE);
				num = 6;
			}
			if (num == 1)
			{
				stringBuilder = new StringBuilder();
				num = 2;
			}
			if (num == 6)
			{
				stringBuilder.AppendLine();
				num = 7;
			}
			if (num == 3)
			{
				stringBuilder.AppendFormat("ValueSize: {0} (0x{0:X})", jQzAxt);
				num = 4;
			}
			if (num == 4)
			{
				stringBuilder.AppendLine();
				num = 5;
			}
			if (num == 2)
			{
				stringBuilder.Append(base.ToString());
				num = 3;
			}
			if (num == 8)
			{
				stringBuilder.AppendLine();
				num = 9;
			}
			if (num == 9)
			{
				stringBuilder.Append(Nm7ch.ToString());
				num = 10;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 10);
		return stringBuilder.ToString();
	}

	public static T0ipHAo cS4(byte[] f2m)
	{
		int num = 0;
		k27Ns k27Ns2 = default;
		EmIig type = default;
		byte[] value = default;
		byte[] bytes = default;
		uint num2 = default;
		uint num3 = default;
		do
		{
			if (num == 14)
			{
				k27Ns2.Nm7ch = new w3F6aB(type, value);
				num = 15;
			}
			if (num == 11)
			{
				k27Ns k27Ns3 = k27Ns2;
				string text = Encoding.Unicode.GetString(bytes);
				char[] trimChars = new char[1];
				k27Ns3.rR2w5VYKU = text.TrimEnd(trimChars);
				num = 12;
			}
			if (num == 13)
			{
				value = f2m.Skip((int)(9 + num2)).Take((int)(num3 - 9 - (int)num2)).ToArray();
				num = 14;
			}
			if (num == 9)
			{
				throw new ArgumentException($"Size of the NameSize is not equal to {num3} ({f2m.Length - 8})");
			}
			if (num == 2)
			{
				if (f2m.Length >= 9)
				{
					goto IL_0152;
				}
				num = 3;
			}
			if (num == 4)
			{
				goto IL_0152;
			}
			goto IL_016d;
			IL_01e7:
			num2 = BitConverter.ToUInt32(f2m, 4);
			num = 8;
			goto IL_0202;
			IL_016d:
			if (num == 5)
			{
				if (f2m.Length >= num3)
				{
					goto IL_01e7;
				}
				num = 6;
			}
			if (num == 6)
			{
				throw new ArgumentException($"Size of the StringName is not equal to {num3} ({f2m.Length})");
			}
			if (num == 7)
			{
				goto IL_01e7;
			}
			goto IL_0202;
			IL_02c8:
			bytes = f2m.Skip(9).Take((int)num2).ToArray();
			num = 11;
			goto IL_02f1;
			IL_02f1:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0152:
			num3 = BitConverter.ToUInt32(f2m, 0);
			num = 5;
			goto IL_016d;
			IL_0202:
			switch (num)
			{
			case 3:
				throw new ArgumentException($"Size of the StringName is less than 9 ({f2m.Length})");
			case 12:
				type = (EmIig)BitConverter.ToUInt16(f2m, 9);
				num = 13;
				break;
			}
			if (num == 1)
			{
				k27Ns2 = new k27Ns();
				num = 2;
			}
			if (num == 8)
			{
				if (f2m.Length - 9 >= num2)
				{
					goto IL_02c8;
				}
				num = 9;
			}
			if (num == 10)
			{
				goto IL_02c8;
			}
			goto IL_02f1;
		}
		while (num != 15);
		return k27Ns2;
	}
}
