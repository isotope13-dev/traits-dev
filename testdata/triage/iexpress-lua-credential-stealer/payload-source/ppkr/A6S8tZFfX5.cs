using System;
using System.ComponentModel;
using System.Runtime.InteropServices;

namespace ppkr;

public class A6S8tZFfX5
{
	private struct ZUm
	{
		public uint cbSize;

		public uint dwTime;
	}

	private static ZUm lastInPutNfo;

	static A6S8tZFfX5()
	{
		lastInPutNfo = default;
		lastInPutNfo.cbSize = (uint)Marshal.SizeOf(lastInPutNfo);
	}

	[DllImport("User32.dll")]
	private static extern bool GetLastInputInfo(ref ZUm plii);

	public static bool WBZZ11Sc0Ep(int EuwPzDkcb)
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
		return Zmn() > EuwPzDkcb;
	}

	public static uint Zmn()
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
			return (uint)Environment.TickCount - Ur1s();
		}
		catch
		{
			return 0u;
		}
	}

	public static uint Ur1s()
	{
		int num = 0;
		do
		{
			if (num == 2)
			{
				throw new Win32Exception(Marshal.GetLastWin32Error());
			}
			if (num == 1)
			{
				if (GetLastInputInfo(ref lastInPutNfo))
				{
					break;
				}
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		return lastInPutNfo.dwTime;
	}
}
