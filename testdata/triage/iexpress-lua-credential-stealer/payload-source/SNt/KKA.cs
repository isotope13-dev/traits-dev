using System.Security.Cryptography;

namespace SNt;

public static class KKA
{
	public static byte[] kVYABv(byte[] lAcyBf)
	{
		int num = 0;
		SHA1CryptoServiceProvider sHA1CryptoServiceProvider = default;
		do
		{
			if (num == 1)
			{
				sHA1CryptoServiceProvider = new SHA1CryptoServiceProvider();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
		return sHA1CryptoServiceProvider.ComputeHash(lAcyBf);
	}

	public static byte[] SF1(byte[] Q6Npcj9, byte[] Txr6v1Rwrj)
	{
		int num = 0;
		HMACSHA1 hMACSHA = default;
		do
		{
			if (num == 1)
			{
				hMACSHA = new HMACSHA1(Q6Npcj9);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
		return hMACSHA.ComputeHash(Txr6v1Rwrj);
	}

	public static string RdeE(string _7TiA, int VU8FmZUJ53z)
	{
		int num = 0;
		string text = default;
		do
		{
			if (num == 1)
			{
				text = "";
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
		try
		{
			foreach (char c in _7TiA)
			{
				text += (char)(c ^ VU8FmZUJ53z);
			}
		}
		catch
		{
		}
		return text;
	}
}
