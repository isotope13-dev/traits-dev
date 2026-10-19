using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using F3k8m0yephw;

namespace WrIixAaZGw;

public class _14yLDCZTXkU : b4mNI9OwAVx
{
	[CompilerGenerated]
	private List<_9noGuOuV3Y> PropertyStorage__BackingField;

	public virtual uint Cz2
	{
		get
		{
			uint num = 8u;
			for (int i = 0; i < uOi9et3.Count; i++)
			{
				num += uOi9et3[i].Ki3U0PYQ3;
			}
			return num;
		}
	}

	public List<_9noGuOuV3Y> uOi9et3
	{
		[CompilerGenerated]
		get
		{
			return PropertyStorage__BackingField;
		}
		[CompilerGenerated]
		set
		{
			PropertyStorage__BackingField = value;
		}
	}

	public _14yLDCZTXkU()
	{
		uOi9et3 = new List<_9noGuOuV3Y>();
	}

	public _14yLDCZTXkU(List<_9noGuOuV3Y> SerializedPropertyStorage)
	{
		uOi9et3 = SerializedPropertyStorage;
	}

	public static _14yLDCZTXkU Owv8HM(byte[] U2p)
	{
		int num = 0;
		uint num3 = default;
		uint num2 = default;
		_14yLDCZTXkU obj = default;
		_9noGuOuV3Y item = default;
		do
		{
			switch (num)
			{
			case 6:
				throw new ArgumentException($"Size of the SerializedPropertyStore is less than {num3} ({U2p.Length})");
			case 8:
				num2 = BitConverter.ToUInt32(U2p, 0);
				num = 9;
				break;
			}
			if (num == 13)
			{
				num2 = BitConverter.ToUInt32(U2p, 0);
				num = 14;
			}
			if (num == 11)
			{
				obj.uOi9et3.Add(item);
				num = 12;
			}
			if (num == 3)
			{
				throw new ArgumentException($"Size of the SerializedPropertyStore is less than 8 ({U2p.Length})");
			}
			if (num == 4)
			{
				goto IL_0116;
			}
			goto IL_0131;
			IL_01fc:
			if (num == 5)
			{
				if (U2p.Length >= num3)
				{
					goto IL_01b4;
				}
				num = 6;
			}
			if (num == 10)
			{
				goto IL_0238;
			}
			goto IL_024e;
			IL_0116:
			num3 = BitConverter.ToUInt32(U2p, 0);
			num = 5;
			goto IL_0131;
			IL_0238:
			item = _9noGuOuV3Y.AsGUBGQz4o(U2p);
			num = 11;
			goto IL_024e;
			IL_01b4:
			U2p = U2p.Skip(4).ToArray();
			num = 8;
			goto IL_01d4;
			IL_024e:
			if (num == 2)
			{
				if (U2p.Length >= 8)
				{
					goto IL_0116;
				}
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_01d4:
			if (num == 14)
			{
				goto IL_01e5;
			}
			goto IL_01fc;
			IL_01e5:
			if (num2 <= 5)
			{
				num = 15;
				goto IL_01fc;
			}
			goto IL_0238;
			IL_0131:
			if (num == 1)
			{
				obj = new _14yLDCZTXkU();
				num = 2;
			}
			if (num == 12)
			{
				U2p = U2p.Skip((int)num2).ToArray();
				num = 13;
			}
			if (num == 9)
			{
				goto IL_01e5;
			}
			if (num == 7)
			{
				goto IL_01b4;
			}
			goto IL_01d4;
		}
		while (num != 15);
		return obj;
	}

	public override byte[] GetBytes()
	{
		int num = 0;
		int num2 = default;
		_9noGuOuV3Y obj = default;
		int num3 = default;
		byte[] array = default;
		do
		{
			if (num == 1)
			{
				num2 = 4;
				num = 2;
			}
			if (num == 8)
			{
				num2 += (int)obj.Ki3U0PYQ3;
				num = 9;
			}
			if (num == 4)
			{
				num3 = 0;
				num = 5;
			}
			if (num == 6)
			{
				goto IL_0091;
			}
			goto IL_00b0;
			IL_0091:
			obj = uOi9et3[num3];
			num = 7;
			goto IL_00b0;
			IL_01ab:
			if (num == 9)
			{
				num3++;
				num = 10;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_00b0:
			if (num == 3)
			{
				Buffer.BlockCopy(BitConverter.GetBytes(Cz2), 0, array, 0, 4);
				num = 4;
			}
			if (num == 2)
			{
				array = new byte[Cz2];
				num = 3;
			}
			if (num != 5)
			{
				if (num == 7)
				{
					Buffer.BlockCopy(obj.GetBytes(), 0, array, num2, (int)obj.Ki3U0PYQ3);
					num = 8;
				}
				if (num != 10)
				{
					goto IL_01ab;
				}
			}
			if (num3 < uOi9et3.Count)
			{
				goto IL_0091;
			}
			num = 11;
			goto IL_01ab;
		}
		while (num != 11);
		return array;
	}

	public override string ToString()
	{
		int num = 0;
		StringBuilder stringBuilder = default;
		int num2 = default;
		do
		{
			if (num == 3)
			{
				stringBuilder.AppendFormat("StoreSize: {0} (0x{0X})", Cz2);
				num = 4;
			}
			if (num == 4)
			{
				stringBuilder.AppendLine();
				num = 5;
			}
			if (num == 6 || num == 9)
			{
				if (num2 < uOi9et3.Count)
				{
					goto IL_00ca;
				}
				num = 10;
			}
			if (num == 7)
			{
				goto IL_00ca;
			}
			goto IL_00f4;
			IL_00ca:
			stringBuilder.Append(uOi9et3[num2].ToString());
			num = 8;
			goto IL_00f4;
			IL_00f4:
			if (num == 8)
			{
				num2++;
				num = 9;
			}
			if (num == 2)
			{
				stringBuilder.Append(base.ToString());
				num = 3;
			}
			if (num == 5)
			{
				num2 = 0;
				num = 6;
			}
			if (num == 1)
			{
				stringBuilder = new StringBuilder();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 10);
		return stringBuilder.ToString();
	}
}
