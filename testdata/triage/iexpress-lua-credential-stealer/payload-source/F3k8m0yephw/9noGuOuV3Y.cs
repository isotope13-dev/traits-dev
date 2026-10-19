using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;

namespace F3k8m0yephw;

public class _9noGuOuV3Y : b4mNI9OwAVx
{
	[CompilerGenerated]
	private Guid FormatID__BackingField;

	[CompilerGenerated]
	private List<T0ipHAo> PropertyStorage__BackingField;

	public virtual uint Ki3U0PYQ3
	{
		get
		{
			uint num = 28u;
			for (int i = 0; i < _4SAZp8IZ.Count; i++)
			{
				num += _4SAZp8IZ[i].jQzAxt;
			}
			return num;
		}
	}

	public uint PjFj4AC4E => 1397773105u;

	public Guid DuCv
	{
		[CompilerGenerated]
		get
		{
			return FormatID__BackingField;
		}
		[CompilerGenerated]
		set
		{
			FormatID__BackingField = value;
		}
	}

	public List<T0ipHAo> _4SAZp8IZ
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

	public _9noGuOuV3Y()
	{
		_4SAZp8IZ = new List<T0ipHAo>();
	}

	public _9noGuOuV3Y(List<T0ipHAo> PropertyStorage)
	{
		_4SAZp8IZ = PropertyStorage;
	}

	public override byte[] GetBytes()
	{
		int num = 0;
		Guid formatID = default;
		T0ipHAo t0ipHAo = default;
		byte[] array = default;
		int num2 = default;
		int num3 = default;
		do
		{
			if (num == 5)
			{
				formatID = DuCv;
				num = 6;
			}
			if (num == 10)
			{
				Buffer.BlockCopy(t0ipHAo.GetBytes(), 0, array, num2, (int)t0ipHAo.jQzAxt);
				num = 11;
			}
			if (num == 9)
			{
				goto IL_0084;
			}
			goto IL_00a3;
			IL_00a3:
			if (num != 8)
			{
				if (num == 12)
				{
					num3++;
					num = 13;
				}
				if (num == 2)
				{
					array = new byte[Ki3U0PYQ3];
					num = 3;
				}
				if (num == 3)
				{
					Buffer.BlockCopy(BitConverter.GetBytes(Ki3U0PYQ3), 0, array, 0, 4);
					num = 4;
				}
				if (num == 6)
				{
					Buffer.BlockCopy(formatID.ToByteArray(), 0, array, 8, 16);
					num = 7;
				}
				if (num != 13)
				{
					goto IL_01c3;
				}
			}
			if (num3 < _4SAZp8IZ.Count)
			{
				goto IL_0084;
			}
			num = 14;
			goto IL_01c3;
			IL_0084:
			t0ipHAo = _4SAZp8IZ[num3];
			num = 10;
			goto IL_00a3;
			IL_01c3:
			if (num == 7)
			{
				num3 = 0;
				num = 8;
			}
			if (num == 11)
			{
				num2 += (int)t0ipHAo.jQzAxt;
				num = 12;
			}
			if (num == 4)
			{
				Buffer.BlockCopy(BitConverter.GetBytes(PjFj4AC4E), 0, array, 4, 4);
				num = 5;
			}
			if (num == 1)
			{
				num2 = 24;
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 14);
		return array;
	}

	public override string ToString()
	{
		int num = 0;
		StringBuilder stringBuilder = default;
		int num2 = default;
		do
		{
			if (num == 8)
			{
				stringBuilder.AppendLine();
				num = 9;
			}
			if (num == 12)
			{
				num2++;
				num = 13;
			}
			if (num == 7)
			{
				stringBuilder.AppendFormat("FormatID: {0}", DuCv);
				num = 8;
			}
			if (num == 13)
			{
				goto IL_00a2;
			}
			goto IL_00c2;
			IL_01fe:
			if (num == 4)
			{
				stringBuilder.AppendLine();
				num = 5;
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
			continue;
			IL_01d4:
			stringBuilder.Append(_4SAZp8IZ[num2].ToString());
			num = 12;
			goto IL_01fe;
			IL_00a2:
			if (num2 >= _4SAZp8IZ.Count)
			{
				num = 14;
				goto IL_00c2;
			}
			goto IL_01d4;
			IL_00c2:
			if (num == 2)
			{
				stringBuilder.Append(base.ToString());
				num = 3;
			}
			if (num == 5)
			{
				stringBuilder.AppendFormat("Version: 0x{0:X}", PjFj4AC4E);
				num = 6;
			}
			if (num == 10)
			{
				goto IL_00a2;
			}
			if (num == 3)
			{
				stringBuilder.AppendFormat("StorageSize: {0} (0x{0:X})", Ki3U0PYQ3);
				num = 4;
			}
			if (num == 6)
			{
				stringBuilder.AppendLine();
				num = 7;
			}
			if (num == 9)
			{
				num2 = 0;
				num = 10;
			}
			if (num == 11)
			{
				goto IL_01d4;
			}
			goto IL_01fe;
		}
		while (num != 14);
		return stringBuilder.ToString();
	}

	public static _9noGuOuV3Y AsGUBGQz4o(byte[] AVGOA)
	{
		int num = 0;
		_9noGuOuV3Y obj = default;
		uint num2 = default;
		T0ipHAo item = default;
		byte[] array = default;
		uint num3 = default;
		uint num4 = default;
		Guid formatID = default;
		do
		{
			if (num == 1)
			{
				obj = new _9noGuOuV3Y();
				num = 2;
			}
			if (num == 15)
			{
				goto IL_00ff;
			}
			if (num == 10)
			{
				goto IL_0061;
			}
			goto IL_0078;
			IL_026e:
			num2 = BitConverter.ToUInt32(AVGOA, 0);
			num = 5;
			goto IL_0289;
			IL_0425:
			item = pCdkn.dwgMP5H18V(AVGOA);
			num = 21;
			goto IL_043b;
			IL_0061:
			array = new byte[16];
			num = 11;
			goto IL_0078;
			IL_0078:
			if (num == 19)
			{
				goto IL_02cf;
			}
			if (num == 5)
			{
				if (AVGOA.Length >= num2)
				{
					goto IL_00d3;
				}
				num = 6;
			}
			if (num == 7)
			{
				goto IL_00d3;
			}
			goto IL_00ee;
			IL_02ea:
			if (num == 23)
			{
				num3 = BitConverter.ToUInt32(AVGOA, 0);
				num = 24;
			}
			if (num == 2)
			{
				if (AVGOA.Length >= 28)
				{
					goto IL_026e;
				}
				num = 3;
			}
			if (num == 12)
			{
				obj.DuCv = new Guid(array);
				num = 13;
			}
			if (num == 22)
			{
				AVGOA = AVGOA.Skip((int)num3).ToArray();
				num = 23;
			}
			switch (num)
			{
			case 9:
				throw new ArgumentException($"Version is not equal to {obj.PjFj4AC4E} ({num4})");
			case 11:
				Buffer.BlockCopy(AVGOA, 8, array, 0, array.Length);
				num = 12;
				break;
			}
			if (num == 20)
			{
				goto IL_0425;
			}
			goto IL_043b;
			IL_02cf:
			obj._4SAZp8IZ.Add(item);
			num = 22;
			goto IL_02ea;
			IL_0289:
			if (num == 3)
			{
				throw new ArgumentException($"Size of the SerializedPropertyStorage is less than 28 ({AVGOA.Length})");
			}
			if (num == 21)
			{
				goto IL_02cf;
			}
			goto IL_02ea;
			IL_0247:
			formatID = obj.DuCv;
			num = 17;
			goto IL_025d;
			IL_00d3:
			num4 = BitConverter.ToUInt32(AVGOA, 4);
			num = 8;
			goto IL_00ee;
			IL_00ee:
			if (num == 24)
			{
				goto IL_00ff;
			}
			goto IL_0116;
			IL_00ff:
			if (num3 <= 5)
			{
				num = 25;
				goto IL_0116;
			}
			goto IL_0247;
			IL_025d:
			if (num == 4)
			{
				goto IL_026e;
			}
			goto IL_0289;
			IL_0116:
			if (num == 14)
			{
				num3 = BitConverter.ToUInt32(AVGOA, 0);
				num = 15;
			}
			if (num == 17)
			{
				if (!formatID.Equals(new Guid("{D5CDD505-2E9C-101B-9397-08002B2CF9AE}")))
				{
					goto IL_0425;
				}
				num = 18;
			}
			if (num == 13)
			{
				AVGOA = AVGOA.Skip(24).ToArray();
				num = 14;
			}
			if (num == 18)
			{
				item = k27Ns.cS4(AVGOA);
				num = 19;
			}
			if (num == 6)
			{
				throw new ArgumentException($"Size of the SerializedPropertyStore is less than {num2} ({AVGOA.Length})");
			}
			if (num == 8)
			{
				if (obj.PjFj4AC4E == num4)
				{
					goto IL_0061;
				}
				num = 9;
			}
			if (num == 16)
			{
				goto IL_0247;
			}
			goto IL_025d;
			IL_043b:
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 25);
		return obj;
	}
}
