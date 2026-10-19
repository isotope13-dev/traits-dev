using System;
using System.Runtime.InteropServices;

namespace e1MhKBne;

public struct _3rNFgn1YqqM : IDisposable
{
	public ushort Length;

	public ushort MaximumLength;

	private IntPtr buffer;

	public _3rNFgn1YqqM(string s)
	{
		Length = (ushort)(s.Length * 2);
		MaximumLength = (ushort)(Length + 2);
		buffer = Marshal.StringToHGlobalUni(s);
	}

	public void Dispose()
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				Marshal.FreeHGlobal(buffer);
				num = 2;
			}
			if (num == 2)
			{
				buffer = IntPtr.Zero;
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
	}

	public override string ToString()
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
		return Marshal.PtrToStringUni(buffer);
	}
}
