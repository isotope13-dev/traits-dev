using System;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using QUNmAVKTUt;

namespace F3k8m0yephw;

public class pCdkn : T0ipHAo
{
	[CompilerGenerated]
	private uint ID__BackingField;

	public override uint iD9bDx
	{
		get
		{
			uint num = (uint)Nm7ch.GetBytes().Length;
			return 9 + num;
		}
	}

	public uint YwSazqTq9
	{
		[CompilerGenerated]
		get
		{
			return ID__BackingField;
		}
		[CompilerGenerated]
		set
		{
			ID__BackingField = value;
		}
	}

	public byte osE => 0;

	public pCdkn()
	{
	}

	public pCdkn(uint ID, w3F6aB TypedPropertyValue)
	{
		YwSazqTq9 = ID;
		Nm7ch = TypedPropertyValue;
	}

	public override byte[] GetBytes()
	{
		int num = 0;
		byte[] array = default;
		do
		{
			if (num == 3)
			{
				Buffer.BlockCopy(BitConverter.GetBytes(YwSazqTq9), 0, array, 4, 4);
				num = 4;
			}
			if (num == 2)
			{
				Buffer.BlockCopy(BitConverter.GetBytes(jQzAxt), 0, array, 0, 4);
				num = 3;
			}
			if (num == 1)
			{
				array = new byte[jQzAxt];
				num = 2;
			}
			if (num == 4)
			{
				Buffer.BlockCopy(Nm7ch.GetBytes(), 0, array, 9, Nm7ch.GetBytes().Length);
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
		return array;
	}

	public override string ToString()
	{
		int num = 0;
		StringBuilder stringBuilder = default;
		do
		{
			if (num == 4)
			{
				stringBuilder.AppendLine();
				num = 5;
			}
			if (num == 6)
			{
				stringBuilder.AppendLine();
				num = 7;
			}
			if (num == 2)
			{
				stringBuilder.Append(base.ToString());
				num = 3;
			}
			if (num == 7)
			{
				stringBuilder.Append(Nm7ch.ToString());
				num = 8;
			}
			if (num == 3)
			{
				stringBuilder.AppendFormat("ValueSize: {0} (0x{0:X})", jQzAxt);
				num = 4;
			}
			if (num == 1)
			{
				stringBuilder = new StringBuilder();
				num = 2;
			}
			if (num == 5)
			{
				stringBuilder.AppendFormat("ID: 0x{0:X}", YwSazqTq9);
				num = 6;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 8);
		return stringBuilder.ToString();
	}

	public static T0ipHAo dwgMP5H18V(byte[] eYK)
	{
		int num = 0;
		EmIig type = default;
		uint num2 = default;
		pCdkn pCdkn2 = default;
		byte[] value = default;
		do
		{
			if (num == 8)
			{
				type = (EmIig)BitConverter.ToUInt16(eYK, 9);
				num = 9;
			}
			if (num == 5)
			{
				if (eYK.Length >= num2)
				{
					goto IL_00d7;
				}
				num = 6;
			}
			if (num == 4)
			{
				goto IL_0076;
			}
			goto IL_0091;
			IL_0091:
			if (num == 3)
			{
				throw new ArgumentException($"Size of the StringName is less than 9 ({eYK.Length})");
			}
			if (num == 7)
			{
				goto IL_00d7;
			}
			goto IL_00f7;
			IL_00f7:
			if (num == 1)
			{
				pCdkn2 = new pCdkn();
				num = 2;
			}
			if (num == 10)
			{
				pCdkn2.Nm7ch = new w3F6aB(type, value);
				num = 11;
			}
			if (num == 6)
			{
				throw new ArgumentException($"Size of the StringName is not equal to {num2} ({eYK.Length})");
			}
			if (num == 2)
			{
				if (eYK.Length >= 9)
				{
					goto IL_0076;
				}
				num = 3;
			}
			if (num == 9)
			{
				value = eYK.Skip(13).Take((int)(num2 - 13)).ToArray();
				num = 10;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0076:
			num2 = BitConverter.ToUInt32(eYK, 0);
			num = 5;
			goto IL_0091;
			IL_00d7:
			pCdkn2.YwSazqTq9 = BitConverter.ToUInt32(eYK, 4);
			num = 8;
			goto IL_00f7;
		}
		while (num != 11);
		return pCdkn2;
	}
}
