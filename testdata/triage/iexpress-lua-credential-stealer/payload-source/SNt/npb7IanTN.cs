using System;

namespace SNt;

public class npb7IanTN
{
	public enum yW3vl
	{
		Sequence = 48,
		Integer = 2,
		BitString = 3,
		OctetString = 4,
		Null = 5,
		ObjectIdentifier = 6
	}

	public i0E9 ncGMtyBS(byte[] IKMidvH)
	{
		int num = 0;
		yW3vl yW3vl2 = default;
		i0E9 i0E10 = default;
		int num2 = default;
		byte[] array = default;
		while (true)
		{
			if (num == 13)
			{
				goto IL_001f;
			}
			goto IL_0069;
			IL_0069:
			if (num == 4)
			{
				goto IL_007a;
			}
			goto IL_008c;
			IL_008c:
			int length;
			if (num == 6)
			{
				switch (yW3vl2)
				{
				case yW3vl.Integer:
				{
					i0E10.eWOcOb.Add(new i0E9
					{
						FWxI = yW3vl.Integer,
						wNQQnf4Q = IKMidvH[num2 + 1]
					});
					array = new byte[IKMidvH[num2 + 1]];
					length = ((num2 + 2 + IKMidvH[num2 + 1] > IKMidvH.Length) ? (IKMidvH.Length - (num2 + 2)) : IKMidvH[num2 + 1]);
					Array.Copy(IKMidvH, num2 + 2, array, 0, length);
					i0E9[] array4 = i0E10.eWOcOb.ToArray();
					i0E10.eWOcOb[array4.Length - 1].WCJJ6 = array;
					num2 = num2 + 1 + i0E10.eWOcOb[array4.Length - 1].wNQQnf4Q;
					goto IL_06f0;
				}
				case yW3vl.OctetString:
				{
					i0E10.eWOcOb.Add(new i0E9
					{
						FWxI = yW3vl.OctetString,
						wNQQnf4Q = IKMidvH[num2 + 1]
					});
					array = new byte[IKMidvH[num2 + 1]];
					length = ((num2 + 2 + IKMidvH[num2 + 1] > IKMidvH.Length) ? (IKMidvH.Length - (num2 + 2)) : IKMidvH[num2 + 1]);
					Array.Copy(IKMidvH, num2 + 2, array, 0, length);
					i0E9[] array3 = i0E10.eWOcOb.ToArray();
					i0E10.eWOcOb[array3.Length - 1].WCJJ6 = array;
					num2 = num2 + 1 + i0E10.eWOcOb[array3.Length - 1].wNQQnf4Q;
					goto IL_06f0;
				}
				case yW3vl.ObjectIdentifier:
				{
					i0E10.eWOcOb.Add(new i0E9
					{
						FWxI = yW3vl.ObjectIdentifier,
						wNQQnf4Q = IKMidvH[num2 + 1]
					});
					array = new byte[IKMidvH[num2 + 1]];
					length = ((num2 + 2 + IKMidvH[num2 + 1] > IKMidvH.Length) ? (IKMidvH.Length - (num2 + 2)) : IKMidvH[num2 + 1]);
					Array.Copy(IKMidvH, num2 + 2, array, 0, length);
					i0E9[] array2 = i0E10.eWOcOb.ToArray();
					i0E10.eWOcOb[array2.Length - 1].WCJJ6 = array;
					num2 = num2 + 1 + i0E10.eWOcOb[array2.Length - 1].wNQQnf4Q;
					goto IL_06f0;
				}
				case yW3vl.BitString:
				case yW3vl.Null:
					goto IL_06f0;
				}
				num = 7;
			}
			if (num != 12)
			{
				if (num == 9)
				{
					i0E10.FWxI = yW3vl.Sequence;
					num = 10;
				}
				if (num == 10)
				{
					i0E10.wNQQnf4Q = IKMidvH.Length - (num2 + 2);
					num = 11;
				}
				if (num == 5)
				{
					yW3vl2 = (yW3vl)IKMidvH[num2];
					num = 6;
				}
				if (num == 2)
				{
					num2 = 0;
					num = 3;
				}
				if (num == 7)
				{
					if (yW3vl2 != yW3vl.Sequence)
					{
						goto IL_06f0;
					}
					num = 8;
				}
				if (num == 11)
				{
					array = new byte[i0E10.wNQQnf4Q];
					num = 12;
				}
				if (num == 8)
				{
					if (i0E10.wNQQnf4Q != 0)
					{
						goto IL_001f;
					}
					num = 9;
				}
				if (num != 15)
				{
					goto IL_0240;
				}
			}
			if (array.Length <= IKMidvH.Length - (num2 + 2))
			{
				num = 16;
				goto IL_0240;
			}
			int num3 = IKMidvH.Length - (num2 + 2);
			goto IL_0306;
			IL_0306:
			length = num3;
			Array.Copy(IKMidvH, num2 + 2, array, 0, length);
			i0E10.eWOcOb.Add(ncGMtyBS(array));
			num2 = num2 + 1 + IKMidvH[num2 + 1];
			goto IL_06f0;
			IL_06fe:
			if (num2 >= IKMidvH.Length)
			{
				break;
			}
			goto IL_007a;
			IL_001f:
			i0E10.eWOcOb.Add(new i0E9
			{
				FWxI = yW3vl.Sequence,
				wNQQnf4Q = IKMidvH[num2 + 1]
			});
			num = 14;
			goto IL_0069;
			IL_06f0:
			num2++;
			goto IL_06fe;
			IL_0240:
			if (num == 3)
			{
				goto IL_06fe;
			}
			if (num == 14)
			{
				array = new byte[IKMidvH[num2 + 1]];
				num = 15;
			}
			if (num == 1)
			{
				i0E10 = new i0E9();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num != 16)
			{
				continue;
			}
			num3 = array.Length;
			goto IL_0306;
			IL_007a:
			length = 0;
			num = 5;
			goto IL_008c;
		}
		return i0E10;
	}
}
