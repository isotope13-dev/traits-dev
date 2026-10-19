using System;
using System.Security.Cryptography;

namespace SNt;

public class _0Jvr0
{
	private int BlockSize;

	private uint BlockIndex = 1u;

	private byte[] BufferBytes;

	private int BufferStartIndex;

	private int BufferEndIndex;

	public HMAC HmacAlgorithm;

	public byte[] sSalt;

	public int IterationCount;

	public _0Jvr0(HMAC algorithm, byte[] password, byte[] salt, int iterations)
	{
		HmacAlgorithm = algorithm;
		HmacAlgorithm.Key = password;
		sSalt = salt;
		IterationCount = iterations;
		BlockSize = HmacAlgorithm.HashSize / 8;
		BufferBytes = new byte[BlockSize - 1 + 1];
	}

	public byte[] t6HPwQD(int HZf8FzyXK)
	{
		int num = 0;
		int i = default;
		int num2 = default;
		byte[] array = default;
		while (true)
		{
			if (num == 2)
			{
				i = 0;
				num = 3;
			}
			if (num == 3)
			{
				num2 = BufferEndIndex - BufferStartIndex;
				num = 4;
			}
			if (num == 5)
			{
				if (HZf8FzyXK >= num2)
				{
					goto IL_00c8;
				}
				num = 6;
			}
			if (num == 7)
			{
				BufferStartIndex += HZf8FzyXK;
				num = 8;
			}
			if (num != 9)
			{
				if (num == 6)
				{
					Buffer.BlockCopy(BufferBytes, BufferStartIndex, array, 0, HZf8FzyXK);
					num = 7;
				}
				if (num == 8)
				{
					return array;
				}
				if (num == 4)
				{
					if (num2 <= 0)
					{
						break;
					}
					num = 5;
				}
				if (num == 1)
				{
					array = new byte[HZf8FzyXK - 1 + 1];
					num = 2;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 10)
				{
					break;
				}
				continue;
			}
			goto IL_00c8;
			IL_00c8:
			Buffer.BlockCopy(BufferBytes, BufferStartIndex, array, 0, num2);
			BufferStartIndex = nL1(ref BufferEndIndex, 0);
			i += num2;
			break;
		}
		for (; i < HZf8FzyXK; i += BlockSize)
		{
			int num3 = HZf8FzyXK - i;
			BufferBytes = lSCIZW0C0();
			if (num3 > BlockSize)
			{
				Buffer.BlockCopy(BufferBytes, 0, array, i, BlockSize);
				continue;
			}
			Buffer.BlockCopy(BufferBytes, 0, array, i, num3);
			BufferStartIndex = num3;
			BufferEndIndex = BlockSize;
			return array;
		}
		return array;
	}

	private static T nL1<T>(ref T ZChK7AmrC, T _5OdK2oNv)
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				ZChK7AmrC = _5OdK2oNv;
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
		return _5OdK2oNv;
	}

	public byte[] aoa50OUT(int _44W, string k9hF = "sha512")
	{
		int num = 0;
		int num2 = default;
		byte[] array = default;
		int i = default;
		while (true)
		{
			if (num == 3)
			{
				num2 = BufferEndIndex - BufferStartIndex;
				num = 4;
			}
			if (num == 1)
			{
				array = new byte[_44W];
				num = 2;
			}
			switch (num)
			{
			case 8:
				return array;
			case 7:
				BufferStartIndex += _44W;
				num = 8;
				break;
			}
			if (num != 9)
			{
				if (num == 2)
				{
					i = 0;
					num = 3;
				}
				if (num == 5)
				{
					if (_44W >= num2)
					{
						goto IL_00c4;
					}
					num = 6;
				}
				if (num == 6)
				{
					Buffer.BlockCopy(BufferBytes, BufferStartIndex, array, 0, _44W);
					num = 7;
				}
				if (num == 4)
				{
					if (num2 <= 0)
					{
						break;
					}
					num = 5;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 10)
				{
					break;
				}
				continue;
			}
			goto IL_00c4;
			IL_00c4:
			Buffer.BlockCopy(BufferBytes, BufferStartIndex, array, 0, num2);
			BufferStartIndex = (BufferEndIndex = 0);
			i += num2;
			break;
		}
		for (; i < _44W; i += BlockSize)
		{
			int num3 = _44W - i;
			BufferBytes = lSCIZW0C0();
			if (num3 > BlockSize)
			{
				Buffer.BlockCopy(BufferBytes, 0, array, i, BlockSize);
				continue;
			}
			Buffer.BlockCopy(BufferBytes, 0, array, i, num3);
			BufferStartIndex = num3;
			BufferEndIndex = BlockSize;
			return array;
		}
		return array;
	}

	private byte[] lSCIZW0C0(bool nfg12i = true)
	{
		int num = 0;
		byte[] array = default;
		int num2 = default;
		byte[] array2 = default;
		byte[] array3 = default;
		int num3 = default;
		do
		{
			if (num == 17)
			{
				goto IL_001f;
			}
			goto IL_003a;
			IL_003a:
			switch (num)
			{
			case 19:
				return null;
			case 2:
				Buffer.BlockCopy(sSalt, 0, array, 0, sSalt.Length);
				num = 3;
				break;
			}
			if (num == 9)
			{
				num2 = 0;
				num = 10;
			}
			if (num == 5)
			{
				array2 = array3;
				num = 6;
			}
			if (num == 13)
			{
				goto IL_00ed;
			}
			goto IL_010e;
			IL_001f:
			if (num3 > IterationCount)
			{
				num = 18;
				goto IL_003a;
			}
			goto IL_011f;
			IL_00ed:
			if (num2 > BlockSize - 1)
			{
				num = 14;
				goto IL_010e;
			}
			goto IL_02dd;
			IL_0358:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0303:
			if (num == 18)
			{
				if (BlockIndex != uint.MaxValue)
				{
					break;
				}
				num = 19;
			}
			if (num == 16)
			{
				goto IL_0341;
			}
			goto IL_0358;
			IL_0341:
			num3++;
			num = 17;
			goto IL_0358;
			IL_010e:
			if (num == 8)
			{
				goto IL_011f;
			}
			goto IL_0149;
			IL_0149:
			if (num == 4)
			{
				array3 = HmacAlgorithm.ComputeHash(array);
				num = 5;
			}
			if (num == 15)
			{
				Array.Copy(array2, array3, array3.Length);
				num = 16;
			}
			if (num == 10)
			{
				goto IL_00ed;
			}
			if (num == 12)
			{
				num2++;
				num = 13;
			}
			if (num == 1)
			{
				array = new byte[sSalt.Length + 4];
				num = 2;
			}
			if (num == 14)
			{
				if (!nfg12i)
				{
					goto IL_0341;
				}
				num = 15;
			}
			if (num == 7)
			{
				goto IL_001f;
			}
			if (num == 6)
			{
				num3 = 2;
				num = 7;
			}
			if (num == 3)
			{
				Buffer.BlockCopy(F9Gr6n(BlockIndex), 0, array, sSalt.Length, 4);
				num = 4;
			}
			if (num == 11)
			{
				goto IL_02dd;
			}
			goto IL_0303;
			IL_02dd:
			array2[num2] ^= array3[num2];
			num = 12;
			goto IL_0303;
			IL_011f:
			array3 = HmacAlgorithm.ComputeHash(array3, 0, array3.Length);
			num = 9;
			goto IL_0149;
		}
		while (num != 20);
		BlockIndex++;
		return array2;
	}

	private static byte[] F9Gr6n(uint mxISynenw)
	{
		int num = 0;
		byte[] array = default;
		byte[] bytes = default;
		do
		{
			switch (num)
			{
			case 8:
				return array;
			case 5:
				array[1] = bytes[2];
				num = 6;
				break;
			}
			if (num == 6)
			{
				array[2] = bytes[1];
				num = 7;
			}
			if (num == 1)
			{
				bytes = BitConverter.GetBytes(mxISynenw);
				num = 2;
			}
			if (num == 2)
			{
				if (!BitConverter.IsLittleEndian)
				{
					break;
				}
				num = 3;
			}
			if (num == 4)
			{
				array[0] = bytes[3];
				num = 5;
			}
			if (num == 3)
			{
				array = new byte[4];
				num = 4;
			}
			if (num == 7)
			{
				array[3] = bytes[0];
				num = 8;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 9);
		return bytes;
	}
}
