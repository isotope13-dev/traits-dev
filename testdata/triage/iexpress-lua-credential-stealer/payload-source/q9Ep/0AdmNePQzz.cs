using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Management;
using Microsoft.VisualBasic.Devices;

namespace q9Ep;

public static class _0AdmNePQzz
{
	public enum MEz
	{
		OperatingSystemName,
		ProcessorName,
		AmountOfMemory
	}

	public static string RUJ(MEz RVOJaQ)
	{
		//IL_001f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0028: Expected Obj, but got Unknown
		//IL_0161: Unknown result type (might be due to invalid IL or missing references)
		//IL_016a: Expected Obj, but got Unknown
		int num = 0;
		ComputerInfo val = default;
		IEnumerator<ManagementObject> enumerator = default;
		ManagementObjectSearcher val2 = default;
		MEz mEz = default;
		do
		{
			if (num == 1)
			{
				val = new ComputerInfo();
				num = 2;
			}
			if (num == 5 || num == 9)
			{
				goto IL_0061;
			}
			if (num == 6)
			{
				goto IL_0081;
			}
			goto IL_00a1;
			IL_0081:
			enumerator = ((IEnumerable)val2.Get()).Cast<ManagementObject>().GetEnumerator();
			num = 7;
			goto IL_00a1;
			IL_0061:
			return "";
			IL_01e8:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0184:
			return val.OSFullName;
			IL_00a1:
			if (num == 7)
			{
				try
				{
					if (enumerator.MoveNext())
					{
						ManagementObject current = enumerator.Current;
						return ((ManagementBaseObject)current).GetPropertyValue("Name").ToString();
					}
				}
				finally
				{
					enumerator?.Dispose();
				}
				goto IL_0061;
			}
			if (num == 2)
			{
				val2 = new ManagementObjectSearcher("SELECT * FROM Win32_Processor");
				num = 3;
			}
			if (num == 8)
			{
				goto IL_0184;
			}
			if (num == 3)
			{
				mEz = RVOJaQ;
				num = 4;
			}
			if (num == 4)
			{
				switch (mEz)
				{
				case MEz.ProcessorName:
					break;
				case MEz.AmountOfMemory:
					return Convert.ToString(Math.Round(Convert.ToDouble(val.TotalPhysicalMemory) / 1024.0 / 1024.0, 2)) + " MB";
				case MEz.OperatingSystemName:
					goto IL_0184;
				default:
					goto IL_01df;
				}
				goto IL_0081;
			}
			goto IL_01e8;
			IL_01df:
			num = 5;
			goto IL_01e8;
		}
		while (num != 10);
		string result = default;
		return result;
	}
}
