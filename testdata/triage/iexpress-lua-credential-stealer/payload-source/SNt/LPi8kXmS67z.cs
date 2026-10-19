using System.Security.Cryptography;

namespace SNt;

public class LPi8kXmS67z
{
	private Rijndael objrij;

	public LPi8kXmS67z()
	{
		objrij = Rijndael.Create();
	}

	public byte[] ErzdrnWy(byte[] _0p5T26gMTkp, byte[] nqG33IxA3hF, byte[] _6zT)
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
			objrij.Key = nqG33IxA3hF;
			objrij.IV = _6zT;
			objrij.Mode = CipherMode.CBC;
			objrij.Padding = PaddingMode.PKCS7;
			return objrij.CreateEncryptor().TransformFinalBlock(_0p5T26gMTkp, 0, _0p5T26gMTkp.Length);
		}
		catch
		{
			throw;
		}
	}

	public byte[] eEF7nNODdAE(byte[] MWH6Msb, byte[] sjy, byte[] ixDTkzX)
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
			objrij.Mode = CipherMode.CBC;
			objrij.Key = sjy;
			objrij.IV = ixDTkzX;
			objrij.Padding = PaddingMode.PKCS7;
			return objrij.CreateDecryptor().TransformFinalBlock(MWH6Msb, 0, MWH6Msb.Length);
		}
		catch
		{
			throw;
		}
	}

	public byte[] mgs()
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
		return objrij.Key;
	}

	public byte[] esRZc()
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
		return objrij.IV;
	}
}
