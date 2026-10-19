using System;
using System.Collections;
using System.Linq;
using System.Management;
using System.Security.Cryptography;
using System.Text;

namespace q9Ep;

public static class JSBB9uM7nh
{
	public static string _35Sj5uGoWdV()
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
		string text;
		try
		{
			text = fJNiE(MD5.Create(), _6QGnjaHxJe() + _6Ucr13Ntc() + BHS3uh());
			if (text.Contains(" "))
			{
				text = text.Replace(" ", "");
			}
		}
		catch
		{
			text = "None";
		}
		return text;
	}

	private static string _6Ucr13Ntc()
	{
		//IL_0052: Unknown result type (might be due to invalid IL or missing references)
		//IL_005b: Expected Obj, but got Unknown
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
			string result = string.Empty;
			ManagementClass val = new ManagementClass("win32_processor");
			ManagementObjectCollection instances = val.GetInstances();
			foreach (ManagementObject item in ((IEnumerable)instances).Cast<ManagementObject>())
			{
				result = ((ManagementBaseObject)item).Properties["processorID"].Value.ToString();
			}
			return result;
		}
		catch
		{
			return "31b7ba0e-2740-4ee8-b8b7-4402b942518d";
		}
	}

	private static string BHS3uh()
	{
		//IL_0049: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Expected Obj, but got Unknown
		//IL_007b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0084: Expected Obj, but got Unknown
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
			ManagementClass val = new ManagementClass("Win32_NetworkAdapterConfiguration");
			string text = string.Empty;
			ManagementObjectEnumerator enumerator = val.GetInstances().GetEnumerator();
			try
			{
				while (enumerator.MoveNext())
				{
					ManagementObject val2 = (ManagementObject)enumerator.Current;
					if (text.Equals(string.Empty))
					{
						if (Convert.ToBoolean(((ManagementBaseObject)val2)["IPEnabled"]))
						{
							text = ((ManagementBaseObject)val2)["MacAddress"].ToString();
						}
						val2.Dispose();
					}
					text = text.Replace(":", string.Empty);
				}
			}
			finally
			{
				((IDisposable)enumerator)?.Dispose();
			}
			return text;
		}
		catch
		{
			return "0f351e93-5caa-452e-a0b7-14de4684f854";
		}
	}

	private static string _6QGnjaHxJe()
	{
		//IL_0049: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Expected Obj, but got Unknown
		//IL_007b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0084: Expected Obj, but got Unknown
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
			ManagementClass val = new ManagementClass("Win32_BaseBoard");
			string text = string.Empty;
			ManagementObjectEnumerator enumerator = val.GetInstances().GetEnumerator();
			try
			{
				while (enumerator.MoveNext())
				{
					ManagementObject val2 = (ManagementObject)enumerator.Current;
					text += ((ManagementBaseObject)val2)["SerialNumber"].ToString();
				}
			}
			finally
			{
				((IDisposable)enumerator)?.Dispose();
			}
			return text;
		}
		catch
		{
			return "d7c73d4e-17eb-4b9b-8edb-b08bb54a3956";
		}
	}

	public static string fJNiE(MD5 GFwYTEjmf, string _4KQBAj0)
	{
		int num = 0;
		int num2 = default;
		StringBuilder stringBuilder = default;
		byte[] array = default;
		while (true)
		{
			if (num == 7)
			{
				goto IL_001f;
			}
			goto IL_0049;
			IL_0049:
			if (num == 8)
			{
				num2++;
				num = 9;
			}
			if (num == 2)
			{
				stringBuilder = new StringBuilder();
				num = 3;
			}
			if (num == 6)
			{
				stringBuilder.Append("-");
				num = 7;
			}
			if (num == 1)
			{
				array = GFwYTEjmf.ComputeHash(Encoding.UTF8.GetBytes(_4KQBAj0));
				num = 2;
			}
			if (num == 5)
			{
				goto IL_0103;
			}
			goto IL_0148;
			IL_017c:
			if (num2 <= array.Length - 1)
			{
				goto IL_0103;
			}
			num = 10;
			goto IL_019a;
			IL_0103:
			if (!((num2 % 2 == 0) & (num2 != array.Length - 1) & (num2 > 0)))
			{
				goto IL_001f;
			}
			num = 6;
			goto IL_0148;
			IL_0148:
			if (num == 3)
			{
				num2 = 0;
				num = 4;
			}
			if (num == 9)
			{
				goto IL_017c;
			}
			goto IL_019a;
			IL_019a:
			if (num == 4)
			{
				goto IL_017c;
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
			IL_001f:
			stringBuilder.Append(array[num2].ToString("x2"));
			num = 8;
			goto IL_0049;
		}
		return stringBuilder.ToString().ToUpper();
	}
}
