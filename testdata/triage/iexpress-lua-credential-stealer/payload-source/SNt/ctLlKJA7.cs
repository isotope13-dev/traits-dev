using System.Security.Cryptography;
using System.Text;

namespace SNt;

public static class ctLlKJA7
{
	public static string Lbl(byte[] Er6ttXs7kDv, DataProtectionScope CsJA937ct1 = (DataProtectionScope)0)
	{
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
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
			return Encoding.UTF8.GetString(ProtectedData.Unprotect(Er6ttXs7kDv, (byte[])null, CsJA937ct1));
		}
		catch
		{
			return "";
		}
	}

	public static byte[] c7mw(byte[] SQSDdQ3lm, DataProtectionScope M8lAe = (DataProtectionScope)0)
	{
		//IL_0049: Unknown result type (might be due to invalid IL or missing references)
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
			return ProtectedData.Unprotect(SQSDdQ3lm, (byte[])null, M8lAe);
		}
		catch
		{
			return null;
		}
	}
}
