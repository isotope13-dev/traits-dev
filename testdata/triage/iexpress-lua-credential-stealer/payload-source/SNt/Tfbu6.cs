using System;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using NbuLaJKWyx2;

namespace SNt;

public class Tfbu6
{
	public byte[] lcjRODFxX8p(byte[] XDeiJ3i, byte[] _9ppVgmOhOM1, byte[] tjP, byte[] _9J16B4, byte[] oBIZEyPe)
	{
		int num = 0;
		iI6anJ2Z.pnc8k pPaddingInfo = default;
		IntPtr intPtr = default;
		int pcbResult = default;
		IntPtr hglobal = default;
		IntPtr cFsf00B1d = default;
		uint num2 = default;
		byte[] array = default;
		byte[] array2 = default;
		do
		{
			switch (num)
			{
			case 14:
				throw new CryptographicException("");
			case 3:
				pPaddingInfo = new iI6anJ2Z.pnc8k(_9ppVgmOhOM1, tjP, oBIZEyPe);
				num = 4;
				break;
			}
			if (num == 17)
			{
				iI6anJ2Z.BCryptCloseAlgorithmProvider(intPtr, 0u);
				num = 18;
			}
			switch (num)
			{
			case 8:
				throw new CryptographicException("");
			case 5:
				pcbResult = 0;
				num = 6;
				break;
			}
			if (num == 15)
			{
				goto IL_00e9;
			}
			goto IL_00fc;
			IL_02ef:
			if (num == 16)
			{
				Marshal.FreeHGlobal(hglobal);
				num = 17;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_00e9:
			iI6anJ2Z.BCryptDestroyKey(cFsf00B1d);
			num = 16;
			goto IL_00fc;
			IL_02b6:
			if (num2 == 0)
			{
				goto IL_00e9;
			}
			num = 14;
			goto IL_02c8;
			IL_02d9:
			array = new byte[pcbResult];
			num = 10;
			goto IL_02ef;
			IL_00fc:
			if (num == 11)
			{
				if (num2 != iI6anJ2Z.STATUS_AUTH_TAG_MISMATCH)
				{
					goto IL_02b6;
				}
				num = 12;
			}
			if (num == 10)
			{
				num2 = iI6anJ2Z.BCryptDecrypt(cFsf00B1d, _9J16B4, _9J16B4.Length, ref pPaddingInfo, array2, array2.Length, array, array.Length, ref pcbResult, 0);
				num = 11;
			}
			if (num == 7)
			{
				if (num2 == 0)
				{
					goto IL_02d9;
				}
				num = 8;
			}
			if (num == 4)
			{
				array2 = new byte[Fx75wOvl(intPtr)];
				num = 5;
			}
			if (num == 1)
			{
				intPtr = Cm7EGATXMKt(iI6anJ2Z.BCRYPT_AES_ALGORITHM, iI6anJ2Z.MS_PRIMITIVE_PROVIDER, iI6anJ2Z.BCRYPT_CHAIN_MODE_GCM);
				num = 2;
			}
			if (num == 6)
			{
				num2 = iI6anJ2Z.BCryptDecrypt(cFsf00B1d, _9J16B4, _9J16B4.Length, ref pPaddingInfo, array2, array2.Length, null, 0, ref pcbResult, 0);
				num = 7;
			}
			switch (num)
			{
			case 12:
				throw new CryptographicException("");
			case 2:
				hglobal = Yoykcy(intPtr, XDeiJ3i, out cFsf00B1d);
				num = 3;
				break;
			}
			if (num == 13)
			{
				goto IL_02b6;
			}
			goto IL_02c8;
			IL_02c8:
			if (num == 9)
			{
				goto IL_02d9;
			}
			goto IL_02ef;
		}
		while (num != 18);
		return array;
	}

	private int Fx75wOvl(IntPtr hiKGouxxEj)
	{
		int num = 0;
		byte[] array = default;
		byte[] array2 = default;
		do
		{
			if (num == 2)
			{
				array = new byte[4];
				num = 3;
			}
			if (num == 6)
			{
				array[3] = array2[7];
				num = 7;
			}
			if (num == 3)
			{
				array[0] = array2[4];
				num = 4;
			}
			if (num == 1)
			{
				array2 = v6tniaxR(hiKGouxxEj, iI6anJ2Z.BCRYPT_AUTH_TAG_LENGTH);
				num = 2;
			}
			if (num == 5)
			{
				array[2] = array2[6];
				num = 6;
			}
			if (num == 4)
			{
				array[1] = array2[5];
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 7);
		return BitConverter.ToInt32(array, 0);
	}

	private IntPtr Cm7EGATXMKt(string sR55lUmvYQH, string VYiWXmR, string qeic02yw4)
	{
		int num = 0;
		uint num2 = default;
		IntPtr phAlgorithm = default;
		byte[] bytes = default;
		do
		{
			if (num == 2)
			{
				num2 = iI6anJ2Z.BCryptOpenAlgorithmProvider(out phAlgorithm, sR55lUmvYQH, VYiWXmR, 0u);
				num = 3;
			}
			if (num == 8)
			{
				throw new CryptographicException("");
			}
			if (num == 5)
			{
				goto IL_0078;
			}
			goto IL_0093;
			IL_0078:
			bytes = Encoding.Unicode.GetBytes(qeic02yw4);
			num = 6;
			goto IL_0093;
			IL_0093:
			if (num == 7)
			{
				if (num2 == 0)
				{
					break;
				}
				num = 8;
			}
			if (num == 3)
			{
				if (num2 == 0)
				{
					goto IL_0078;
				}
				num = 4;
			}
			if (num == 1)
			{
				phAlgorithm = IntPtr.Zero;
				num = 2;
			}
			if (num == 6)
			{
				num2 = iI6anJ2Z.BCryptSetAlgorithmProperty(phAlgorithm, iI6anJ2Z.BCRYPT_CHAINING_MODE, bytes, bytes.Length, 0);
				num = 7;
			}
			switch (num)
			{
			case 4:
				throw new CryptographicException("");
			case 0:
				num = 1;
				break;
			}
		}
		while (num != 9);
		return phAlgorithm;
	}

	private IntPtr Yoykcy(IntPtr zLdcxlvee, byte[] sc6Ak29RN, out IntPtr cFsf00B1d)
	{
		int num = 0;
		uint num2 = default;
		IntPtr intPtr = default;
		int num3 = default;
		byte[] value = default;
		byte[] array = default;
		do
		{
			if (num == 6)
			{
				if (num2 == 0)
				{
					break;
				}
				num = 7;
			}
			if (num == 3)
			{
				intPtr = Marshal.AllocHGlobal(num3);
				num = 4;
			}
			if (num == 2)
			{
				num3 = BitConverter.ToInt32(value, 0);
				num = 3;
			}
			if (num == 4)
			{
				array = k4Bz7wtTcKE(iI6anJ2Z.BCRYPT_KEY_DATA_BLOB_MAGIC, BitConverter.GetBytes(1), BitConverter.GetBytes(sc6Ak29RN.Length), sc6Ak29RN);
				num = 5;
			}
			switch (num)
			{
			case 7:
				throw new CryptographicException("");
			case 5:
				num2 = iI6anJ2Z.BCryptImportKey(zLdcxlvee, IntPtr.Zero, iI6anJ2Z.BCRYPT_KEY_DATA_BLOB, out cFsf00B1d, intPtr, num3, array, array.Length, 0u);
				num = 6;
				break;
			}
			if (num == 1)
			{
				value = v6tniaxR(zLdcxlvee, iI6anJ2Z.BCRYPT_OBJECT_LENGTH);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 8);
		return intPtr;
	}

	private byte[] v6tniaxR(IntPtr _3w8WJFT8Xx, string zSOFRtc7l)
	{
		int num = 0;
		uint num2 = default;
		int pcbResult = default;
		byte[] array = default;
		do
		{
			if (num == 5)
			{
				goto IL_001f;
			}
			goto IL_0035;
			IL_0035:
			if (num == 8)
			{
				throw new CryptographicException("");
			}
			if (num == 4)
			{
				throw new CryptographicException("");
			}
			if (num == 7)
			{
				if (num2 == 0)
				{
					break;
				}
				num = 8;
			}
			if (num == 3)
			{
				if (num2 == 0)
				{
					goto IL_001f;
				}
				num = 4;
			}
			if (num == 1)
			{
				pcbResult = 0;
				num = 2;
			}
			if (num == 6)
			{
				num2 = iI6anJ2Z.BCryptGetProperty(_3w8WJFT8Xx, zSOFRtc7l, array, array.Length, ref pcbResult, 0u);
				num = 7;
			}
			if (num == 2)
			{
				num2 = iI6anJ2Z.BCryptGetProperty(_3w8WJFT8Xx, zSOFRtc7l, null, 0, ref pcbResult, 0u);
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_001f:
			array = new byte[pcbResult];
			num = 6;
			goto IL_0035;
		}
		while (num != 9);
		return array;
	}

	public byte[] k4Bz7wtTcKE(params byte[][] YU6etjag1)
	{
		int num = 0;
		int num2 = default;
		byte[] array = default;
		byte[] array2 = default;
		int num3 = default;
		int num4 = default;
		byte[] array3 = default;
		byte[][] array4 = default;
		int num5 = default;
		byte[][] array5 = default;
		do
		{
			if (num == 11)
			{
				num2 = 0;
				num = 12;
			}
			if (num == 17)
			{
				Buffer.BlockCopy(array, 0, array2, num2, array.Length);
				num = 18;
			}
			if (num == 3)
			{
				num3 = 0;
				num = 4;
			}
			if (num == 1)
			{
				num4 = 0;
				num = 2;
			}
			if (num == 4)
			{
				goto IL_01ba;
			}
			if (num == 6)
			{
				if (array3 == null)
				{
					goto IL_0100;
				}
				num = 7;
			}
			if (num == 8)
			{
				goto IL_0100;
			}
			goto IL_0117;
			IL_0117:
			if (num == 14)
			{
				goto IL_01e3;
			}
			if (num == 18)
			{
				num2 += array.Length;
				num = 19;
			}
			if (num == 12)
			{
				array4 = YU6etjag1;
				num = 13;
			}
			if (num == 19)
			{
				goto IL_0192;
			}
			goto IL_01a9;
			IL_0100:
			num3++;
			num = 9;
			goto IL_0117;
			IL_0192:
			num5++;
			num = 20;
			goto IL_01a9;
			IL_02c4:
			array = array4[num5];
			num = 16;
			goto IL_02da;
			IL_022e:
			array3 = array5[num3];
			num = 6;
			goto IL_0244;
			IL_01fb:
			if (num == 2)
			{
				array5 = YU6etjag1;
				num = 3;
			}
			if (num == 5)
			{
				goto IL_022e;
			}
			goto IL_0244;
			IL_01a9:
			if (num == 9)
			{
				goto IL_01ba;
			}
			goto IL_01d2;
			IL_02da:
			if (num == 10)
			{
				array2 = new byte[num4 - 1 + 1];
				num = 11;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_01ba:
			if (num3 >= array5.Length)
			{
				num = 10;
				goto IL_01d2;
			}
			goto IL_022e;
			IL_01d2:
			if (num == 20)
			{
				goto IL_01e3;
			}
			goto IL_01fb;
			IL_01e3:
			if (num5 >= array4.Length)
			{
				num = 21;
				goto IL_01fb;
			}
			goto IL_02c4;
			IL_0244:
			if (num == 7)
			{
				num4 += array3.Length;
				num = 8;
			}
			if (num == 13)
			{
				num5 = 0;
				num = 14;
			}
			if (num == 16)
			{
				if (array == null)
				{
					goto IL_0192;
				}
				num = 17;
			}
			if (num == 15)
			{
				goto IL_02c4;
			}
			goto IL_02da;
		}
		while (num != 21);
		return array2;
	}
}
