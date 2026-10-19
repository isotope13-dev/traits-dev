using System;
using System.Security.Cryptography;
using System.Text;

namespace SNt;

public class _3VzYbXLJt4
{
	public string CpTvsYwz(string Xrq90tW, string yffj7dP9)
	{
		int num = 0;
		UTF8Encoding uTF8Encoding = default;
		byte[] inArray;
		MD5CryptoServiceProvider mD5CryptoServiceProvider = default;
		do
		{
			if (num == 2)
			{
				uTF8Encoding = new UTF8Encoding();
				num = 3;
			}
			if (num == 1)
			{
				inArray = null;
				num = 2;
			}
			if (num == 3)
			{
				mD5CryptoServiceProvider = new MD5CryptoServiceProvider();
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		try
		{
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
			tripleDESCryptoServiceProvider.Key = mD5CryptoServiceProvider.ComputeHash(uTF8Encoding.GetBytes(yffj7dP9));
			tripleDESCryptoServiceProvider.Mode = CipherMode.ECB;
			tripleDESCryptoServiceProvider.Padding = PaddingMode.PKCS7;
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider2 = tripleDESCryptoServiceProvider;
			byte[] bytes = uTF8Encoding.GetBytes(Xrq90tW);
			try
			{
				ICryptoTransform cryptoTransform = tripleDESCryptoServiceProvider2.CreateEncryptor();
				inArray = cryptoTransform.TransformFinalBlock(bytes, 0, bytes.Length);
			}
			finally
			{
				tripleDESCryptoServiceProvider2.Clear();
				mD5CryptoServiceProvider.Clear();
			}
		}
		finally
		{
			((IDisposable)mD5CryptoServiceProvider)?.Dispose();
		}
		return Convert.ToBase64String(inArray);
	}

	public static string VGqCJfFX(string ULx5EUXL, byte[] TleRa0, byte[] oQlBFMDwJCp)
	{
		int num = 0;
		string s = default;
		do
		{
			if (num == 2)
			{
				if (ULx5EUXL[0] != '_')
				{
					break;
				}
				num = 3;
			}
			if (num == 1)
			{
				s = ULx5EUXL;
				num = 2;
			}
			if (num == 3)
			{
				s = ULx5EUXL.Substring(1);
				num = 4;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		try
		{
			byte[] array = Convert.FromBase64String(s);
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
			tripleDESCryptoServiceProvider.Key = TleRa0;
			tripleDESCryptoServiceProvider.Mode = CipherMode.CBC;
			tripleDESCryptoServiceProvider.IV = oQlBFMDwJCp;
			tripleDESCryptoServiceProvider.Padding = PaddingMode.None;
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider2 = tripleDESCryptoServiceProvider;
			byte[] bytes = tripleDESCryptoServiceProvider2.CreateDecryptor().TransformFinalBlock(array, 0, array.Length);
			return Encoding.UTF8.GetString(bytes);
		}
		catch
		{
			return null;
		}
	}

	public static string fOLl(byte[] RYKw3aKM, byte[] C6XEEp0De, byte[] dWeHH)
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
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
			tripleDESCryptoServiceProvider.Key = C6XEEp0De;
			tripleDESCryptoServiceProvider.Mode = CipherMode.CBC;
			tripleDESCryptoServiceProvider.IV = dWeHH;
			tripleDESCryptoServiceProvider.Padding = PaddingMode.None;
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider2 = tripleDESCryptoServiceProvider;
			byte[] bytes = tripleDESCryptoServiceProvider2.CreateDecryptor().TransformFinalBlock(RYKw3aKM, 0, RYKw3aKM.Length);
			return Encoding.UTF8.GetString(bytes);
		}
		catch
		{
			return null;
		}
	}

	public static byte[] wBp(byte[] qMHA3, byte[] CpMvzbyTKHY, byte[] _89S)
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
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
			tripleDESCryptoServiceProvider.Key = CpMvzbyTKHY;
			tripleDESCryptoServiceProvider.Mode = CipherMode.CBC;
			tripleDESCryptoServiceProvider.IV = _89S;
			tripleDESCryptoServiceProvider.Padding = PaddingMode.None;
			TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider2 = tripleDESCryptoServiceProvider;
			return tripleDESCryptoServiceProvider2.CreateDecryptor().TransformFinalBlock(qMHA3, 0, qMHA3.Length);
		}
		catch
		{
			return null;
		}
	}
}
