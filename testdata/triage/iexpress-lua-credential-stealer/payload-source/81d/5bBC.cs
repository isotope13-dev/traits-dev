using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using e1MhKBne;

namespace _81d;

public class _5bBC
{
	private struct qLR8CiAEI
	{
		public long size;

		public long type;
	}

	private struct JKwJ8
	{
		public long row_id;

		public string item_type;

		public string item_name;

		public string astable_name;

		public long root_num;

		public string sql_statement;
	}

	private struct uSAE7Dg
	{
		public long row_id;

		public string[] content;
	}

	private readonly byte[] db_bytes;

	private readonly ulong encoding;

	private readonly ushort page_size;

	private readonly byte[] SQLDataTypeSize = new byte[10] { 0, 1, 2, 3, 4, 6, 8, 8, 0, 0 };

	public string[] field_names = new string[1];

	private JKwJ8[] master_table_entries;

	private uSAE7Dg[] table_entries;

	public _5bBC(string baseName)
	{
		if (!File.Exists(baseName))
		{
			return;
		}
		db_bytes = DQBx6eo2(baseName);
		if (db_bytes != null && db_bytes.Length >= 1 && Encoding.Default.GetString(db_bytes, 0, 15).CompareTo("SQLite format 3") == 0 && db_bytes[52] == 0)
		{
			page_size = (ushort)hND(16, 2);
			encoding = hND(56, 4);
			if (decimal.Compare(new decimal(encoding), 0m) == 0)
			{
				encoding = 1uL;
			}
			f0W3Y(100uL);
		}
	}

	private byte[] DQBx6eo2(string hKkSv7)
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
			byte[] array = null;
			using (FileStream fileStream = new FileStream(hKkSv7, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
			{
				array = new byte[fileStream.Length - 1 + 1];
				fileStream.Read(array, 0, Convert.ToInt32(fileStream.Length));
			}
			return array;
		}
		catch
		{
			return HaAVOPYT._3ggy(hKkSv7);
		}
	}

	private ulong hND(int H8hy2Z, int bnog5EbwbQE)
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				if (!((bnog5EbwbQE > 8) | (bnog5EbwbQE == 0)))
				{
					break;
				}
				num = 2;
			}
			switch (num)
			{
			case 2:
				return 0uL;
			case 0:
				num = 1;
				break;
			}
		}
		while (num != 3);
		ulong num2 = 0uL;
		int num3 = bnog5EbwbQE - 1;
		for (int i = 0; i <= num3; i++)
		{
			num2 = (num2 << 8) | db_bytes[H8hy2Z + i];
		}
		return num2;
	}

	private long VtTgN(int QScX, int NCMF)
	{
		int num = 0;
		int num2 = default;
		bool flag = default;
		byte[] array = default;
		while (true)
		{
			if (num == 3)
			{
				num2 = NCMF - QScX;
				num = 4;
			}
			if (num == 6)
			{
				return 0L;
			}
			if (num != 7)
			{
				if (num == 1)
				{
					NCMF++;
					num = 2;
				}
				if (num == 4)
				{
					flag = false;
					num = 5;
				}
				if (num == 2)
				{
					array = new byte[8];
					num = 3;
				}
				if (num == 5)
				{
					if (!((num2 == 0) | (num2 > 9)))
					{
						goto IL_0067;
					}
					num = 6;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 8)
				{
					break;
				}
				continue;
			}
			goto IL_0067;
			IL_0067:
			if (num2 != 1)
			{
				break;
			}
			array[0] = (byte)(db_bytes[QScX] & 0x7F);
			return BitConverter.ToInt64(array, 0);
		}
		if (num2 == 9)
		{
			flag = true;
		}
		int num3 = 1;
		int num4 = 7;
		int num5 = 0;
		if (flag)
		{
			array[0] = db_bytes[NCMF - 1];
			NCMF--;
			num5 = 1;
		}
		for (int i = NCMF - 1; i >= QScX; i += -1)
		{
			if (i - 1 >= QScX)
			{
				array[num5] = (byte)(((byte)(db_bytes[i] >> ((num3 - 1) & 7)) & (255 >> num3)) | (byte)(db_bytes[i - 1] << (num4 & 7)));
				num3++;
				num5++;
				num4--;
			}
			else if (!flag)
			{
				array[num5] = (byte)((byte)(db_bytes[i] >> ((num3 - 1) & 7)) & (255 >> num3));
			}
		}
		return BitConverter.ToInt64(array, 0);
	}

	public int FtN5geM()
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
		return table_entries.Length;
	}

	public string[] qBPf0()
	{
		int num = 0;
		int num2 = default;
		int num3 = default;
		List<string> list = default;
		while (true)
		{
			if (num == 5)
			{
				goto IL_001f;
			}
			goto IL_004e;
			IL_004e:
			if (num == 3)
			{
				num2 = 0;
				num = 4;
			}
			if (num == 2)
			{
				num3 = master_table_entries.Length - 1;
				num = 3;
			}
			if (num == 8)
			{
				goto IL_00b1;
			}
			goto IL_00c7;
			IL_014c:
			if (num == 4)
			{
				goto IL_00b1;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 9)
			{
				break;
			}
			continue;
			IL_00b1:
			if (num2 <= num3)
			{
				goto IL_001f;
			}
			num = 9;
			goto IL_00c7;
			IL_0135:
			num2++;
			num = 8;
			goto IL_014c;
			IL_001f:
			if (master_table_entries[num2].item_type == "table")
			{
				num = 6;
				goto IL_004e;
			}
			goto IL_0135;
			IL_00c7:
			if (num == 6)
			{
				list.Add(master_table_entries[num2].item_name);
				num = 7;
			}
			if (num == 1)
			{
				list = new List<string>();
				num = 2;
			}
			if (num == 7)
			{
				goto IL_0135;
			}
			goto IL_014c;
		}
		return list.ToArray();
	}

	public string gzd4rqxbTqm(int hEf, int es99qs)
	{
		int num = 0;
		while (true)
		{
			if (num == 2)
			{
				return null;
			}
			if (num != 3)
			{
				if (num == 1)
				{
					if (hEf < table_entries.Length)
					{
						goto IL_003b;
					}
					num = 2;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 4)
				{
					break;
				}
				continue;
			}
			goto IL_003b;
			IL_003b:
			if (es99qs < table_entries[hEf].content.Length)
			{
				break;
			}
			return null;
		}
		return table_entries[hEf].content[es99qs];
	}

	public string Jw0(int FzM3ucc, string SuHeYooZhS)
	{
		int num = 0;
		int num2 = default;
		int num3 = default;
		int num4 = default;
		while (true)
		{
			if (num == 8)
			{
				goto IL_001f;
			}
			goto IL_0036;
			IL_0036:
			if (num == 1)
			{
				num2 = -1;
				num = 2;
			}
			if (num == 4)
			{
				goto IL_00f8;
			}
			if (num == 2)
			{
				num3 = field_names.Length - 1;
				num = 3;
			}
			if (num == 5)
			{
				goto IL_00b8;
			}
			goto IL_00e7;
			IL_00b8:
			if (field_names[num4].ToLower().CompareTo(SuHeYooZhS.ToLower()) != 0)
			{
				goto IL_001f;
			}
			num = 6;
			goto IL_00e7;
			IL_0136:
			if (num == 3)
			{
				num4 = 0;
				num = 4;
			}
			if (num == 11)
			{
				return null;
			}
			if (num == 7)
			{
				goto IL_011f;
			}
			if (num == 6)
			{
				num2 = num4;
				num = 7;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 12)
			{
				break;
			}
			continue;
			IL_011f:
			if (num2 != -1)
			{
				break;
			}
			num = 11;
			goto IL_0136;
			IL_010e:
			if (num == 10)
			{
				goto IL_011f;
			}
			goto IL_0136;
			IL_001f:
			num4++;
			num = 9;
			goto IL_0036;
			IL_00e7:
			if (num == 9)
			{
				goto IL_00f8;
			}
			goto IL_010e;
			IL_00f8:
			if (num4 <= num3)
			{
				goto IL_00b8;
			}
			num = 10;
			goto IL_010e;
		}
		return gzd4rqxbTqm(FzM3ucc, num2);
	}

	private int _7ItPgg(int _0TywUI0)
	{
		int num = 0;
		int num2 = default;
		int num3 = default;
		while (true)
		{
			if (num == 3)
			{
				goto IL_001f;
			}
			if (num == 4)
			{
				goto IL_0074;
			}
			if (num == 2)
			{
				return 0;
			}
			if (num == 1)
			{
				if (_0TywUI0 <= db_bytes.Length)
				{
					goto IL_001f;
				}
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 5)
			{
				goto IL_0124;
			}
			continue;
			IL_0132:
			if (num2 > num3)
			{
				break;
			}
			if (num2 > db_bytes.Length - 1)
			{
				return 0;
			}
			goto IL_0074;
			IL_0124:
			num2++;
			goto IL_0132;
			IL_001f:
			num3 = _0TywUI0 + 8;
			num2 = _0TywUI0;
			goto IL_0132;
			IL_0074:
			if ((db_bytes[num2] & 0x80) != 128)
			{
				return num2;
			}
			goto IL_0124;
		}
		return _0TywUI0 + 8;
	}

	private bool smHx(long oENMqWOkVC)
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
		return (oENMqWOkVC & 1) == 1;
	}

	private void f0W3Y(ulong jpWOlI)
	{
		int num = 0;
		ushort num2 = default;
		int num3 = default;
		int num4 = default;
		ulong num5 = default;
		long value = default;
		long[] array = default;
		int num6 = default;
		ushort num7 = default;
		int num8 = default;
		int num9 = default;
		int num10 = default;
		int num11 = default;
		ushort num12 = default;
		int num13 = default;
		do
		{
			if (num == 57)
			{
				goto IL_001f;
			}
			goto IL_004a;
			IL_004a:
			if (num == 50)
			{
				goto IL_1298;
			}
			if (num == 7)
			{
				goto IL_0b36;
			}
			if (num == 72)
			{
				f0W3Y(Convert.ToUInt64(decimal.Multiply(decimal.Subtract(new decimal(hND(num2, 4)), 1m), new decimal(page_size))));
				num = 73;
			}
			if (num == 64)
			{
				break;
			}
			if (num == 51)
			{
				goto IL_0115;
			}
			goto IL_0140;
			IL_1298:
			master_table_entries[num3 + num4].root_num = (long)hND(Convert.ToInt32(decimal.Add(decimal.Add(decimal.Add(decimal.Add(new decimal(num5), new decimal(value)), new decimal(array[0])), new decimal(array[1])), new decimal(array[2]))), (int)array[3]);
			num = 54;
			goto IL_1329;
			IL_0b36:
			num6 = num7;
			num = 10;
			goto IL_0b47;
			IL_06e0:
			if (num == 52)
			{
				master_table_entries[num3 + num4].item_name = Encoding.BigEndianUnicode.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num5), new decimal(value)), new decimal(array[0]))), (int)array[1]);
				num = 53;
			}
			if (num == 38)
			{
				master_table_entries[num3 + num4].item_type = Encoding.Default.GetString(db_bytes, Convert.ToInt32(decimal.Add(new decimal(num5), new decimal(value))), (int)array[0]);
				num = 39;
			}
			if (num == 17)
			{
				num8 = _7ItPgg(Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num5), decimal.Subtract(new decimal(num9), new decimal(num5))), 1m)));
				num = 18;
			}
			if (num == 36)
			{
				if (num10 <= 4)
				{
					goto IL_0240;
				}
				num = 37;
			}
			if (num == 30)
			{
				array[num10] = (long)Math.Round((double)(array[num10] - 13) / 2.0);
				num = 31;
			}
			if (num == 68)
			{
				num11 = 0;
				num = 69;
			}
			if (num == 33)
			{
				goto IL_1270;
			}
			if (num == 44)
			{
				master_table_entries[num3 + num4].item_type = Encoding.BigEndianUnicode.GetString(db_bytes, Convert.ToInt32(decimal.Add(new decimal(num5), new decimal(value))), (int)array[0]);
				num = 45;
			}
			if (num == 6)
			{
				Array.Resize(ref master_table_entries, master_table_entries.Length + num7 + 1);
				num = 7;
			}
			if (num == 37)
			{
				if (decimal.Compare(new decimal(encoding), 1m) != 0)
				{
					goto IL_0ace;
				}
				num = 38;
			}
			if (num == 32)
			{
				goto IL_09de;
			}
			goto IL_0a12;
			IL_06bf:
			master_table_entries = new JKwJ8[num7 + 1];
			num = 9;
			goto IL_06e0;
			IL_1287:
			if (num == 53)
			{
				goto IL_1298;
			}
			goto IL_1329;
			IL_0140:
			if (num == 43)
			{
				goto IL_0151;
			}
			goto IL_017c;
			IL_017c:
			if (num == 66)
			{
				num12 = Convert.ToUInt16(decimal.Subtract(new decimal(hND(Convert.ToInt32(decimal.Add(new decimal(jpWOlI), 3m)), 2)), 1m));
				num = 67;
			}
			if (num == 10)
			{
				num4 = 0;
				num = 11;
			}
			if (num == 28)
			{
				if (array[num10] <= 9)
				{
					goto IL_0c00;
				}
				num = 29;
			}
			if (num == 25)
			{
				goto IL_0240;
			}
			goto IL_0257;
			IL_034a:
			if (decimal.Compare(new decimal(encoding), 1m) == 0)
			{
				num = 46;
				goto IL_0375;
			}
			goto IL_0d03;
			IL_0b47:
			if (num == 2)
			{
				num7 = Convert.ToUInt16(decimal.Subtract(new decimal(hND(Convert.ToInt32(decimal.Add(new decimal(jpWOlI), 3m)), 2)), 1m));
				num = 3;
			}
			if (num == 42)
			{
				goto IL_034a;
			}
			if (num == 76)
			{
				goto IL_0bd9;
			}
			goto IL_0bef;
			IL_1056:
			if (decimal.Compare(new decimal(encoding), 3m) == 0)
			{
				num = 61;
				goto IL_1081;
			}
			goto IL_133a;
			IL_001f:
			if (decimal.Compare(new decimal(encoding), 2m) == 0)
			{
				num = 58;
				goto IL_004a;
			}
			goto IL_1056;
			IL_0fa1:
			if (num == 75)
			{
				goto IL_0fb2;
			}
			goto IL_0fc9;
			IL_052a:
			num2 = (ushort)hND(Convert.ToInt32(decimal.Add(decimal.Add(new decimal(jpWOlI), 12m), new decimal(num11 * 2))), 2);
			num = 71;
			goto IL_0577;
			IL_1270:
			num10++;
			num = 36;
			goto IL_1287;
			IL_0257:
			if (num == 58)
			{
				master_table_entries[num3 + num4].sql_statement = Encoding.Unicode.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(decimal.Add(decimal.Add(decimal.Add(new decimal(num5), new decimal(value)), new decimal(array[0])), new decimal(array[1])), new decimal(array[2])), new decimal(array[3]))), (int)array[4]);
				num = 59;
			}
			if (num == 67)
			{
				num13 = num12;
				num = 68;
			}
			if (num == 45)
			{
				goto IL_034a;
			}
			goto IL_0375;
			IL_0bd9:
			if (num11 <= num13)
			{
				goto IL_052a;
			}
			num = 77;
			goto IL_0bef;
			IL_0240:
			num9 = num8 + 1;
			num = 26;
			goto IL_0257;
			IL_0bef:
			if (num == 34)
			{
				goto IL_0c00;
			}
			goto IL_0c27;
			IL_0c00:
			array[num10] = SQLDataTypeSize[(int)array[num10]];
			num = 35;
			goto IL_0c27;
			IL_0375:
			if (num == 13)
			{
				if (decimal.Compare(new decimal(jpWOlI), 100m) == 0)
				{
					goto IL_0fda;
				}
				num = 14;
			}
			if (num == 23)
			{
				array = new long[5];
				num = 24;
			}
			if (num == 16)
			{
				VtTgN((int)num5, num9);
				num = 17;
			}
			if (num == 4)
			{
				if (master_table_entries == null)
				{
					goto IL_06bf;
				}
				num = 5;
			}
			if (num == 39)
			{
				goto IL_034a;
			}
			if (num == 14)
			{
				num5 += jpWOlI;
				num = 15;
			}
			if (num == 24)
			{
				num10 = 0;
				num = 25;
			}
			if (num == 31)
			{
				goto IL_1270;
			}
			if (num == 74)
			{
				goto IL_04c2;
			}
			goto IL_0519;
			IL_0c27:
			if (num == 41)
			{
				master_table_entries[num3 + num4].item_type = Encoding.Unicode.GetString(db_bytes, Convert.ToInt32(decimal.Add(new decimal(num5), new decimal(value))), (int)array[0]);
				num = 42;
			}
			if (num == 22)
			{
				value = VtTgN((int)num5, num9);
				num = 23;
			}
			if (num == 26)
			{
				num8 = _7ItPgg(num9);
				num = 27;
			}
			if (num == 48)
			{
				goto IL_0d03;
			}
			goto IL_0d2e;
			IL_0fb2:
			num11++;
			num = 76;
			goto IL_0fc9;
			IL_0fc9:
			if (num == 15)
			{
				goto IL_0fda;
			}
			goto IL_0ff5;
			IL_0ff5:
			if (num == 63)
			{
				goto IL_1006;
			}
			goto IL_101c;
			IL_0fda:
			num9 = _7ItPgg((int)num5);
			num = 16;
			goto IL_0ff5;
			IL_1329:
			if (num == 62)
			{
				goto IL_133a;
			}
			goto IL_1351;
			IL_1006:
			if (num4 <= num6)
			{
				goto IL_0f55;
			}
			num = 64;
			goto IL_101c;
			IL_0115:
			if (decimal.Compare(new decimal(encoding), 3m) == 0)
			{
				num = 52;
				goto IL_0140;
			}
			goto IL_1298;
			IL_0d03:
			if (decimal.Compare(new decimal(encoding), 2m) != 0)
			{
				goto IL_0115;
			}
			num = 49;
			goto IL_0d2e;
			IL_0f55:
			num5 = hND(Convert.ToInt32(decimal.Add(decimal.Add(new decimal(jpWOlI), 8m), new decimal(num4 * 2))), 2);
			num = 13;
			goto IL_0fa1;
			IL_0a12:
			if (num == 29)
			{
				if (!smHx(array[num10]))
				{
					goto IL_09de;
				}
				num = 30;
			}
			if (num == 77)
			{
				f0W3Y(Convert.ToUInt64(decimal.Multiply(decimal.Subtract(new decimal(hND(Convert.ToInt32(decimal.Add(new decimal(jpWOlI), 8m)), 4)), 1m), new decimal(page_size))));
				num = 78;
			}
			if (num == 40)
			{
				goto IL_0ace;
			}
			goto IL_0af9;
			IL_1351:
			if (num == 54)
			{
				if (decimal.Compare(new decimal(encoding), 1m) != 0)
				{
					goto IL_001f;
				}
				num = 55;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0d2e:
			if (num == 71)
			{
				if (decimal.Compare(new decimal(jpWOlI), 100m) != 0)
				{
					goto IL_04c2;
				}
				num = 72;
			}
			if (num == 55)
			{
				master_table_entries[num3 + num4].sql_statement = Encoding.Default.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(decimal.Add(decimal.Add(decimal.Add(new decimal(num5), new decimal(value)), new decimal(array[0])), new decimal(array[1])), new decimal(array[2])), new decimal(array[3]))), (int)array[4]);
				num = 56;
			}
			if (num == 46)
			{
				master_table_entries[num3 + num4].item_name = Encoding.Default.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num5), new decimal(value)), new decimal(array[0]))), (int)array[1]);
				num = 47;
			}
			if (num == 18)
			{
				master_table_entries[num3 + num4].row_id = VtTgN(Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num5), decimal.Subtract(new decimal(num9), new decimal(num5))), 1m)), num8);
				num = 19;
			}
			if (num == 11)
			{
				goto IL_1006;
			}
			if (num == 12)
			{
				goto IL_0f55;
			}
			goto IL_0fa1;
			IL_101c:
			if (num == 5)
			{
				num3 = master_table_entries.Length;
				num = 6;
			}
			if (num == 60)
			{
				goto IL_1056;
			}
			goto IL_1081;
			IL_09de:
			array[num10] = (long)Math.Round((double)(array[num10] - 12) / 2.0);
			num = 33;
			goto IL_0a12;
			IL_04c2:
			f0W3Y(Convert.ToUInt64(decimal.Multiply(decimal.Subtract(new decimal(hND((int)(jpWOlI + num2), 4)), 1m), new decimal(page_size))));
			num = 75;
			goto IL_0519;
			IL_0519:
			if (num == 70)
			{
				goto IL_052a;
			}
			goto IL_0577;
			IL_0577:
			if (num == 69)
			{
				goto IL_0bd9;
			}
			if (num == 49)
			{
				master_table_entries[num3 + num4].item_name = Encoding.Unicode.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num5), new decimal(value)), new decimal(array[0]))), (int)array[1]);
				num = 50;
			}
			if (num == 27)
			{
				array[num10] = VtTgN(num9, num8);
				num = 28;
			}
			if (num == 21)
			{
				num8 = num9;
				num = 22;
			}
			if (num == 56)
			{
				goto IL_133a;
			}
			if (num == 73)
			{
				goto IL_0fb2;
			}
			if (num == 8)
			{
				goto IL_06bf;
			}
			goto IL_06e0;
			IL_1081:
			if (num == 65)
			{
				goto IL_1092;
			}
			goto IL_10b4;
			IL_1092:
			if (db_bytes[(uint)jpWOlI] == 5)
			{
				num = 66;
				goto IL_10b4;
			}
			break;
			IL_0ace:
			if (decimal.Compare(new decimal(encoding), 2m) != 0)
			{
				goto IL_0151;
			}
			num = 41;
			goto IL_0af9;
			IL_133a:
			num4++;
			num = 63;
			goto IL_1351;
			IL_0151:
			if (decimal.Compare(new decimal(encoding), 3m) == 0)
			{
				num = 44;
				goto IL_017c;
			}
			goto IL_034a;
			IL_10b4:
			if (num == 3)
			{
				num3 = 0;
				num = 4;
			}
			if (num == 61)
			{
				master_table_entries[num3 + num4].sql_statement = Encoding.BigEndianUnicode.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(decimal.Add(decimal.Add(decimal.Add(new decimal(num5), new decimal(value)), new decimal(array[0])), new decimal(array[1])), new decimal(array[2])), new decimal(array[3]))), (int)array[4]);
				num = 62;
			}
			if (num == 19)
			{
				num5 = Convert.ToUInt64(decimal.Add(decimal.Add(new decimal(num5), decimal.Subtract(new decimal(num8), new decimal(num5))), 1m));
				num = 20;
			}
			if (num == 1)
			{
				if (db_bytes[(uint)jpWOlI] != 13)
				{
					goto IL_1092;
				}
				num = 2;
			}
			if (num == 47)
			{
				goto IL_1298;
			}
			if (num == 59)
			{
				goto IL_133a;
			}
			if (num == 35)
			{
				goto IL_1270;
			}
			goto IL_1287;
			IL_0af9:
			if (num == 20)
			{
				num9 = _7ItPgg((int)num5);
				num = 21;
			}
			if (num == 9)
			{
				goto IL_0b36;
			}
			goto IL_0b47;
		}
		while (num != 78);
	}

	public bool ga9(string O6CRubv2)
	{
		int num = 0;
		int num2 = default;
		int num3 = default;
		int num4 = default;
		while (true)
		{
			if (num == 1)
			{
				num2 = -1;
				num = 2;
			}
			if (num == 3)
			{
				num3 = 0;
				num = 4;
			}
			if (num == 6)
			{
				num2 = num3;
				num = 7;
			}
			if (num == 5)
			{
				goto IL_0087;
			}
			goto IL_00bf;
			IL_00e6:
			if (num == 8)
			{
				goto IL_00f7;
			}
			goto IL_010e;
			IL_00bf:
			if (num == 9)
			{
				goto IL_00d0;
			}
			goto IL_00e6;
			IL_00d0:
			if (num3 <= num4)
			{
				goto IL_0087;
			}
			num = 10;
			goto IL_00e6;
			IL_010e:
			if (num == 2)
			{
				num4 = master_table_entries.Length - 1;
				num = 3;
			}
			if (num == 11)
			{
				return false;
			}
			if (num == 4)
			{
				goto IL_00d0;
			}
			if (num == 7 || num == 10)
			{
				if (num2 != -1)
				{
					break;
				}
				num = 11;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 12)
			{
				break;
			}
			continue;
			IL_00f7:
			num3++;
			num = 9;
			goto IL_010e;
			IL_0087:
			if (master_table_entries[num3].item_name.ToLower().CompareTo(O6CRubv2.ToLower()) == 0)
			{
				num = 6;
				goto IL_00bf;
			}
			goto IL_00f7;
		}
		string[] array = master_table_entries[num2].sql_statement.Substring(master_table_entries[num2].sql_statement.IndexOf("(") + 1).Split(new char[1] { ',' });
		int num5 = array.Length - 1;
		for (int i = 0; i <= num5; i++)
		{
			array[i] = array[i].TrimStart(new char[0]);
			if (array[i].EndsWith(")"))
			{
				array[i] = array[i].Substring(0, array[i].Length - 1);
			}
			int num6 = array[i].IndexOf(" ");
			if (num6 > 0)
			{
				array[i] = array[i].Substring(0, num6);
			}
			if (array[i].IndexOf("UNIQUE") == 0)
			{
				break;
			}
			Array.Resize(ref field_names, i + 1);
			field_names[i] = array[i];
		}
		return hiJS5fRfQdv((ulong)((master_table_entries[num2].root_num - 1) * page_size));
	}

	private bool hiJS5fRfQdv(ulong vWCcanD6KpQ)
	{
		int num = 0;
		int num2 = default;
		int num3 = default;
		qLR8CiAEI[] array = default;
		ulong num4 = default;
		int num5 = default;
		ushort num6 = default;
		int num7 = default;
		ushort num8 = default;
		int num9 = default;
		int num10 = default;
		long num11 = default;
		int num12 = default;
		int num13 = default;
		int num14 = default;
		int num15 = default;
		int num16 = default;
		long num17 = default;
		int num18 = default;
		while (true)
		{
			if (num == 41)
			{
				table_entries[num2 + num3].content = new string[array.Length - 1 + 1];
				num = 42;
			}
			if (num != 36)
			{
				if (num == 15)
				{
					num4 += vWCcanD6KpQ;
					num = 16;
				}
				if (num != 38)
				{
					goto IL_00d5;
				}
			}
			goto IL_00b2;
			IL_107e:
			if (num == 65)
			{
				break;
			}
			if (num == 68)
			{
				num5 = num6;
				num = 69;
			}
			if (num == 14)
			{
				if (decimal.Compare(new decimal(vWCcanD6KpQ), 100m) == 0)
				{
					goto IL_0c3b;
				}
				num = 15;
			}
			if (num == 70)
			{
				goto IL_03ac;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 76)
			{
				break;
			}
			continue;
			IL_0b21:
			array[num7].size = (long)Math.Round((double)(array[num7].type - 12) / 2.0);
			num = 36;
			goto IL_0b67;
			IL_0216:
			num8 = (ushort)hND(Convert.ToInt32(decimal.Add(decimal.Add(new decimal(vWCcanD6KpQ), 12m), new decimal(num9 * 2))), 2);
			num = 72;
			goto IL_0263;
			IL_0daa:
			if (num == 52)
			{
				table_entries[num2 + num3].content[num10] = Encoding.Unicode.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num4), new decimal(num11)), new decimal(num12))), (int)array[num10].size);
				num = 53;
			}
			if (num != 56)
			{
				if (num == 5)
				{
					num2 = table_entries.Length;
					num = 6;
				}
				if (num == 6)
				{
					Array.Resize(ref table_entries, table_entries.Length + num13 + 1);
					num = 7;
				}
				if (num != 53 && num != 50)
				{
					if (num == 12)
					{
						goto IL_0f0a;
					}
					goto IL_0f21;
				}
			}
			goto IL_0a58;
			IL_0c67:
			if (num10 > num14)
			{
				num = 63;
				goto IL_0c7d;
			}
			goto IL_0cb6;
			IL_00d5:
			if (num == 54)
			{
				goto IL_00e6;
			}
			goto IL_0111;
			IL_0111:
			if (num == 8)
			{
				goto IL_0122;
			}
			goto IL_0143;
			IL_0143:
			if (num == 18)
			{
				num15 = _7ItPgg(Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num4), decimal.Subtract(new decimal(num16), new decimal(num4))), 1m)));
				num = 19;
			}
			if (num == 67)
			{
				num6 = Convert.ToUInt16(decimal.Subtract(new decimal(hND(Convert.ToInt32(decimal.Add(new decimal(vWCcanD6KpQ), 3m)), 2)), 1m));
				num = 68;
			}
			if (num == 71)
			{
				goto IL_0216;
			}
			goto IL_0263;
			IL_0f0a:
			array = new qLR8CiAEI[1];
			num = 13;
			goto IL_0f21;
			IL_00b2:
			num17 = num17 + (num15 - num16) + 1;
			num = 39;
			goto IL_00d5;
			IL_0c56:
			if (num == 62)
			{
				goto IL_0c67;
			}
			goto IL_0c7d;
			IL_0f21:
			if (num == 49)
			{
				table_entries[num2 + num3].content[num10] = Encoding.Default.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num4), new decimal(num11)), new decimal(num12))), (int)array[num10].size);
				num = 50;
			}
			if (num == 33)
			{
				array[num7].size = (long)Math.Round((double)(array[num7].type - 13) / 2.0);
				num = 34;
			}
			if (num == 28)
			{
				num16 = num15 + 1;
				num = 29;
			}
			if (num == 21)
			{
				num16 = _7ItPgg((int)num4);
				num = 22;
			}
			if (num == 64)
			{
				goto IL_1068;
			}
			goto IL_107e;
			IL_0263:
			if (num == 23)
			{
				num11 = VtTgN((int)num4, num16);
				num = 24;
			}
			if (num == 72)
			{
				hiJS5fRfQdv(Convert.ToUInt64(decimal.Multiply(decimal.Subtract(new decimal(hND((int)(vWCcanD6KpQ + num8), 4)), 1m), new decimal(page_size))));
				num = 73;
			}
			if (num == 45)
			{
				goto IL_0c67;
			}
			if (num == 42)
			{
				num12 = 0;
				num = 43;
			}
			if (num == 47)
			{
				if (smHx(array[num10].type))
				{
					goto IL_03d3;
				}
				num = 48;
			}
			if (num == 25)
			{
				num7 = 0;
				num = 26;
			}
			if (num == 74)
			{
				goto IL_03ac;
			}
			goto IL_03c2;
			IL_0c7d:
			if (num == 39)
			{
				num7++;
				num = 40;
			}
			if (num == 46)
			{
				goto IL_0cb6;
			}
			goto IL_0cdc;
			IL_0a1a:
			if (num == 27)
			{
				goto IL_0a2b;
			}
			goto IL_0a47;
			IL_0a47:
			if (num == 60)
			{
				goto IL_0a58;
			}
			goto IL_0a7d;
			IL_0a7d:
			if (num == 40)
			{
				goto IL_0a8e;
			}
			goto IL_0aa4;
			IL_0c3b:
			num16 = _7ItPgg((int)num4);
			num = 17;
			goto IL_0c56;
			IL_0578:
			if (decimal.Compare(new decimal(encoding), 2m) != 0)
			{
				goto IL_00e6;
			}
			num = 52;
			goto IL_05a3;
			IL_0a2b:
			Array.Resize(ref array, num7 + 1);
			num = 28;
			goto IL_0a47;
			IL_00e6:
			if (decimal.Compare(new decimal(encoding), 3m) == 0)
			{
				num = 55;
				goto IL_0111;
			}
			goto IL_0a58;
			IL_0cb6:
			if (array[num10].type <= 9)
			{
				goto IL_09a5;
			}
			num = 47;
			goto IL_0cdc;
			IL_0a58:
			num12 += (int)array[num10].size;
			num = 61;
			goto IL_0a7d;
			IL_0ab5:
			array[num7].size = SQLDataTypeSize[(int)array[num7].type];
			num = 38;
			goto IL_0aee;
			IL_0a8e:
			if (num17 < num11)
			{
				goto IL_0a2b;
			}
			num = 41;
			goto IL_0aa4;
			IL_03c2:
			if (num == 57)
			{
				goto IL_03d3;
			}
			goto IL_044d;
			IL_03d3:
			table_entries[num2 + num3].content[num10] = Encoding.Default.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num4), new decimal(num11)), new decimal(num12))), (int)array[num10].size);
			num = 58;
			goto IL_044d;
			IL_044d:
			if (num == 44)
			{
				num10 = 0;
				num = 45;
			}
			if (num == 2)
			{
				num13 = Convert.ToInt32(decimal.Subtract(new decimal(hND(Convert.ToInt32(decimal.Add(new decimal(vWCcanD6KpQ), 3m)), 2)), 1m));
				num = 3;
			}
			if (num == 17)
			{
				VtTgN((int)num4, num16);
				num = 18;
			}
			if (num == 26)
			{
				goto IL_0a8e;
			}
			if (num == 24)
			{
				num17 = Convert.ToInt64(decimal.Add(decimal.Subtract(new decimal(num4), new decimal(num16)), 1m));
				num = 25;
			}
			if (num == 51)
			{
				goto IL_0578;
			}
			goto IL_05a3;
			IL_0b10:
			if (num == 35)
			{
				goto IL_0b21;
			}
			goto IL_0b67;
			IL_0aa4:
			if (num == 37)
			{
				goto IL_0ab5;
			}
			goto IL_0aee;
			IL_0122:
			table_entries = new uSAE7Dg[num13 + 1];
			num = 9;
			goto IL_0143;
			IL_0b67:
			if (num == 43)
			{
				num14 = array.Length - 1;
				num = 44;
			}
			if (num == 30)
			{
				array[num7].type = VtTgN(num16, num15);
				num = 31;
			}
			if (num == 32)
			{
				if (!smHx(array[num7].type))
				{
					goto IL_0b21;
				}
				num = 33;
			}
			if (num == 22)
			{
				num15 = num16;
				num = 23;
			}
			if (num == 16)
			{
				goto IL_0c3b;
			}
			goto IL_0c56;
			IL_09a5:
			table_entries[num2 + num3].content[num10] = Convert.ToString(hND(Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num4), new decimal(num11)), new decimal(num12))), (int)array[num10].size));
			num = 60;
			goto IL_0a1a;
			IL_0aee:
			if (num == 9)
			{
				goto IL_0aff;
			}
			goto IL_0b10;
			IL_0cdc:
			if (num == 7)
			{
				goto IL_0aff;
			}
			if (num == 19)
			{
				table_entries[num2 + num3].row_id = VtTgN(Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num4), decimal.Subtract(new decimal(num16), new decimal(num4))), 1m)), num15);
				num = 20;
			}
			if (num == 66)
			{
				goto IL_0d88;
			}
			goto IL_0daa;
			IL_0aff:
			num18 = num13;
			num = 10;
			goto IL_0b10;
			IL_03ac:
			if (num9 <= num5)
			{
				goto IL_0216;
			}
			num = 75;
			goto IL_03c2;
			IL_05a3:
			if (num == 75)
			{
				hiJS5fRfQdv(Convert.ToUInt64(decimal.Multiply(decimal.Subtract(new decimal(hND(Convert.ToInt32(decimal.Add(new decimal(vWCcanD6KpQ), 8m)), 4)), 1m), new decimal(page_size))));
				num = 76;
			}
			if (num == 1)
			{
				if (db_bytes[(uint)vWCcanD6KpQ] != 13)
				{
					goto IL_0d88;
				}
				num = 2;
			}
			if (num == 20)
			{
				num4 = Convert.ToUInt64(decimal.Add(decimal.Add(new decimal(num4), decimal.Subtract(new decimal(num15), new decimal(num4))), 1m));
				num = 21;
			}
			if (num == 34)
			{
				goto IL_00b2;
			}
			if (num == 61)
			{
				num10++;
				num = 62;
			}
			if (num == 73)
			{
				num9++;
				num = 74;
			}
			if (num == 13)
			{
				num4 = hND(Convert.ToInt32(decimal.Add(decimal.Add(new decimal(vWCcanD6KpQ), 8m), new decimal(num3 * 2))), 2);
				num = 14;
			}
			if (num == 48)
			{
				if (decimal.Compare(new decimal(encoding), 1m) != 0)
				{
					goto IL_0578;
				}
				num = 49;
			}
			if (num == 69)
			{
				num9 = 0;
				num = 70;
			}
			if (num == 4)
			{
				if (table_entries == null)
				{
					goto IL_0122;
				}
				num = 5;
			}
			if (num == 55)
			{
				table_entries[num2 + num3].content[num10] = Encoding.BigEndianUnicode.GetString(db_bytes, Convert.ToInt32(decimal.Add(decimal.Add(new decimal(num4), new decimal(num11)), new decimal(num12))), (int)array[num10].size);
				num = 56;
			}
			if (num == 11)
			{
				goto IL_1068;
			}
			if (num == 58)
			{
				goto IL_0a58;
			}
			if (num == 3)
			{
				num2 = 0;
				num = 4;
			}
			if (num == 63)
			{
				num3++;
				num = 64;
			}
			if (num == 29)
			{
				num15 = _7ItPgg(num16);
				num = 30;
			}
			if (num == 31)
			{
				if (array[num7].type <= 9)
				{
					goto IL_0ab5;
				}
				num = 32;
			}
			if (num == 10)
			{
				num3 = 0;
				num = 11;
			}
			if (num == 59)
			{
				goto IL_09a5;
			}
			goto IL_0a1a;
			IL_1068:
			if (num3 <= num18)
			{
				goto IL_0f0a;
			}
			num = 65;
			goto IL_107e;
			IL_0d88:
			if (db_bytes[(uint)vWCcanD6KpQ] != 5)
			{
				break;
			}
			num = 67;
			goto IL_0daa;
		}
		return true;
	}
}
