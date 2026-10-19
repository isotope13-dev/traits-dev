using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Text;

namespace SNt;

public class i0E9
{
	[CompilerGenerated]
	private npb7IanTN.yW3vl Type__BackingField;

	[CompilerGenerated]
	private int Lenght__BackingField;

	[CompilerGenerated]
	private List<i0E9> objects__BackingField;

	[CompilerGenerated]
	private byte[] Data__BackingField;

	public npb7IanTN.yW3vl FWxI
	{
		[CompilerGenerated]
		get
		{
			return Type__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Type__BackingField = value;
		}
	}

	public int wNQQnf4Q
	{
		[CompilerGenerated]
		get
		{
			return Lenght__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Lenght__BackingField = value;
		}
	}

	public List<i0E9> eWOcOb
	{
		[CompilerGenerated]
		get
		{
			return objects__BackingField;
		}
		[CompilerGenerated]
		set
		{
			objects__BackingField = value;
		}
	}

	public byte[] WCJJ6
	{
		[CompilerGenerated]
		get
		{
			return Data__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Data__BackingField = value;
		}
	}

	public i0E9()
	{
		eWOcOb = new List<i0E9>();
	}

	public override string ToString()
	{
		int num = 0;
		int num2 = default;
		StringBuilder stringBuilder = default;
		byte b = default;
		npb7IanTN.yW3vl type = default;
		StringBuilder stringBuilder2 = default;
		int num3 = default;
		byte b2 = default;
		byte[] data = default;
		int num4 = default;
		byte[] data2 = default;
		List<i0E9>.Enumerator enumerator = default;
		byte[] data3 = default;
		byte b3 = default;
		do
		{
			if (num == 23)
			{
				num2++;
				num = 24;
			}
			if (num == 36)
			{
				stringBuilder = new StringBuilder();
				num = 37;
			}
			if (num == 22)
			{
				stringBuilder.AppendFormat("{0:X2}", b);
				num = 23;
			}
			if (num == 31)
			{
				goto IL_009c;
			}
			goto IL_00b2;
			IL_056e:
			if (num == 4)
			{
				switch (type)
				{
				case npb7IanTN.yW3vl.BitString:
				case npb7IanTN.yW3vl.Null:
					break;
				case npb7IanTN.yW3vl.OctetString:
					goto IL_02a9;
				case npb7IanTN.yW3vl.Integer:
					goto IL_0371;
				case npb7IanTN.yW3vl.ObjectIdentifier:
					goto IL_0422;
				default:
					goto IL_05a2;
				}
				goto IL_016e;
			}
			goto IL_05ab;
			IL_01f4:
			if (num == 16)
			{
				stringBuilder = new StringBuilder();
				num = 17;
			}
			if (num == 21)
			{
				goto IL_0228;
			}
			goto IL_023e;
			IL_023e:
			if (num == 25)
			{
				stringBuilder2.AppendLine("\tOCTETSTRING " + stringBuilder.ToString());
				num = 26;
			}
			if (num == 9)
			{
				num3 = 0;
				num = 10;
			}
			if (num == 18)
			{
				goto IL_02a9;
			}
			goto IL_02bf;
			IL_0387:
			if (num == 6)
			{
				stringBuilder2.AppendLine("SEQUENCE {");
				num = 7;
			}
			if (num == 17)
			{
				goto IL_016e;
			}
			if (num == 20)
			{
				goto IL_00c3;
			}
			if (num == 26)
			{
				stringBuilder = new StringBuilder();
				num = 27;
			}
			if (num == 28)
			{
				goto IL_0422;
			}
			goto IL_0438;
			IL_0558:
			b2 = data[num3];
			num = 12;
			goto IL_056e;
			IL_05a2:
			num = 5;
			goto IL_05ab;
			IL_00b2:
			if (num == 24)
			{
				goto IL_00c3;
			}
			goto IL_00db;
			IL_00db:
			if (num == 33)
			{
				num4++;
				num = 34;
			}
			if (num == 35)
			{
				stringBuilder2.AppendLine("\tOBJECTIDENTIFIER " + stringBuilder.ToString());
				num = 36;
			}
			if (num == 19)
			{
				num2 = 0;
				num = 20;
			}
			if (num == 37)
			{
				goto IL_016e;
			}
			goto IL_0189;
			IL_00c3:
			if (num2 >= data2.Length)
			{
				num = 25;
				goto IL_00db;
			}
			goto IL_0228;
			IL_05d4:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0228:
			b = data2[num2];
			num = 22;
			goto IL_023e;
			IL_02bf:
			if (num == 7)
			{
				goto IL_016e;
			}
			if (num == 13)
			{
				num3++;
				num = 14;
			}
			if (num == 15)
			{
				stringBuilder2.AppendLine("\tINTEGER " + stringBuilder);
				num = 16;
			}
			if (num == 5)
			{
				if (type != npb7IanTN.yW3vl.Sequence)
				{
					goto IL_016e;
				}
				num = 6;
			}
			if (num == 8)
			{
				goto IL_0371;
			}
			goto IL_0387;
			IL_0371:
			data = WCJJ6;
			num = 9;
			goto IL_0387;
			IL_016e:
			enumerator = eWOcOb.GetEnumerator();
			num = 38;
			goto IL_0189;
			IL_0189:
			if (num != 30)
			{
				if (num == 1)
				{
					stringBuilder2 = new StringBuilder();
					num = 2;
				}
				if (num != 34)
				{
					goto IL_01f4;
				}
			}
			if (num4 < data3.Length)
			{
				goto IL_009c;
			}
			num = 35;
			goto IL_01f4;
			IL_0422:
			data3 = WCJJ6;
			num = 29;
			goto IL_0438;
			IL_05bc:
			if (num3 < data.Length)
			{
				goto IL_0558;
			}
			num = 15;
			goto IL_05d4;
			IL_05ab:
			if (num == 14)
			{
				goto IL_05bc;
			}
			goto IL_05d4;
			IL_0438:
			if (num == 27)
			{
				goto IL_016e;
			}
			if (num == 3)
			{
				type = FWxI;
				num = 4;
			}
			if (num == 12)
			{
				stringBuilder.AppendFormat("{0:X2}", b2);
				num = 13;
			}
			if (num == 10)
			{
				goto IL_05bc;
			}
			if (num == 2)
			{
				stringBuilder = new StringBuilder();
				num = 3;
			}
			if (num == 29)
			{
				num4 = 0;
				num = 30;
			}
			if (num == 32)
			{
				stringBuilder.AppendFormat("{0:X2}", b3);
				num = 33;
			}
			if (num == 11)
			{
				goto IL_0558;
			}
			goto IL_056e;
			IL_02a9:
			data2 = WCJJ6;
			num = 19;
			goto IL_02bf;
			IL_009c:
			b3 = data3[num4];
			num = 32;
			goto IL_00b2;
		}
		while (num != 38);
		try
		{
			while (enumerator.MoveNext())
			{
				i0E9 current = enumerator.Current;
				stringBuilder2.Append(current.ToString());
			}
		}
		finally
		{
			((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
		}
		if (FWxI.Equals(npb7IanTN.yW3vl.Sequence))
		{
			stringBuilder2.AppendLine("}");
		}
		return stringBuilder2.ToString();
	}
}
