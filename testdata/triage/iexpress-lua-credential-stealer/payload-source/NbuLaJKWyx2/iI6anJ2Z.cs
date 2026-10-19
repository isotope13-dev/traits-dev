using System;
using System.Runtime.InteropServices;

namespace NbuLaJKWyx2;

public static class iI6anJ2Z
{
	public struct vHmX2UAX(string pszAlgId, int cbSalt)
	{
		[MarshalAs(UnmanagedType.LPWStr)]
		public string pszAlgId = pszAlgId;

		public int cbSalt = cbSalt;
	}

	public struct pnc8k : IDisposable
	{
		public int cbSize;

		public int dwInfoVersion;

		public IntPtr pbNonce;

		public int cbNonce;

		public IntPtr pbAuthData;

		public int cbAuthData;

		public IntPtr pbTag;

		public int cbTag;

		public IntPtr pbMacContext;

		public int cbMacContext;

		public int cbAAD;

		public long cbData;

		public int dwFlags;

		public pnc8k(byte[] iv, byte[] aad, byte[] tag)
		{
			this = default;
			dwInfoVersion = BCRYPT_INIT_AUTH_MODE_INFO_VERSION;
			cbSize = Marshal.SizeOf(typeof(pnc8k));
			if (iv != null)
			{
				cbNonce = iv.Length;
				pbNonce = Marshal.AllocHGlobal(cbNonce);
				Marshal.Copy(iv, 0, pbNonce, cbNonce);
			}
			if (aad != null)
			{
				cbAuthData = aad.Length;
				pbAuthData = Marshal.AllocHGlobal(cbAuthData);
				Marshal.Copy(aad, 0, pbAuthData, cbAuthData);
			}
			if (tag != null)
			{
				cbTag = tag.Length;
				pbTag = Marshal.AllocHGlobal(cbTag);
				Marshal.Copy(tag, 0, pbTag, cbTag);
				cbMacContext = tag.Length;
				pbMacContext = Marshal.AllocHGlobal(cbMacContext);
			}
		}

		public void Dispose()
		{
			if (pbNonce != IntPtr.Zero)
			{
				Marshal.FreeHGlobal(pbNonce);
			}
			if (pbTag != IntPtr.Zero)
			{
				Marshal.FreeHGlobal(pbTag);
			}
			if (pbAuthData != IntPtr.Zero)
			{
				Marshal.FreeHGlobal(pbAuthData);
			}
			if (pbMacContext != IntPtr.Zero)
			{
				Marshal.FreeHGlobal(pbMacContext);
			}
		}
	}

	public struct iqtz8qA
	{
		public int dwMinLength;

		public int dwMaxLength;

		public int dwIncrement;
	}

	public struct vXZrx(string alg)
	{
		[MarshalAs(UnmanagedType.LPWStr)]
		public string pszAlgId = alg;

		public IntPtr pbLabel = IntPtr.Zero;

		public int cbLabel = 0;
	}

	public enum _8Zyn2YXtHnZ
	{
		Generic = 1,
		DomainPassword = 2,
		DomainCertificate = 3,
		GenericCertificate = 5,
		DomainExtended = 6,
		Maximum = 7,
		MaximumEx = 1007
	}

	[Flags]
	public enum gIo3Gkhe17a
	{
		IS_TEXT_UNICODE_ASCII16 = 1,
		IS_TEXT_UNICODE_REVERSE_ASCII16 = 0x10,
		IS_TEXT_UNICODE_STATISTICS = 2,
		IS_TEXT_UNICODE_REVERSE_STATISTICS = 0x20,
		IS_TEXT_UNICODE_CONTROLS = 4,
		IS_TEXT_UNICODE_REVERSE_CONTROLS = 0x40,
		IS_TEXT_UNICODE_SIGNATURE = 8,
		IS_TEXT_UNICODE_REVERSE_SIGNATURE = 0x80,
		IS_TEXT_UNICODE_ILLEGAL_CHARS = 0x100,
		IS_TEXT_UNICODE_ODD_LENGTH = 0x200,
		IS_TEXT_UNICODE_DBCS_LEADBYTE = 0x400,
		IS_TEXT_UNICODE_NULL_BYTES = 0x1000,
		IS_TEXT_UNICODE_UNICODE_MASK = IS_TEXT_UNICODE_ASCII16 | IS_TEXT_UNICODE_STATISTICS | IS_TEXT_UNICODE_CONTROLS | IS_TEXT_UNICODE_SIGNATURE,
		IS_TEXT_UNICODE_REVERSE_MASK = IS_TEXT_UNICODE_REVERSE_ASCII16 | IS_TEXT_UNICODE_REVERSE_STATISTICS | IS_TEXT_UNICODE_REVERSE_CONTROLS | IS_TEXT_UNICODE_REVERSE_SIGNATURE,
		IS_TEXT_UNICODE_NOT_UNICODE_MASK = 0xF00,
		IS_TEXT_UNICODE_NOT_ASCII_MASK = 0xF000
	}

	public const uint ERROR_SUCCESS = 0u;

	public const uint BCRYPT_PAD_PSS = 8u;

	public const uint BCRYPT_PAD_OAEP = 4u;

	public static readonly byte[] BCRYPT_KEY_DATA_BLOB_MAGIC = BitConverter.GetBytes(1296188491);

	public static readonly string BCRYPT_OBJECT_LENGTH = "ObjectLength";

	public static readonly string BCRYPT_CHAIN_MODE_GCM = "ChainingModeGCM";

	public static readonly string BCRYPT_AUTH_TAG_LENGTH = "AuthTagLength";

	public static readonly string BCRYPT_CHAINING_MODE = "ChainingMode";

	public static readonly string BCRYPT_KEY_DATA_BLOB = "KeyDataBlob";

	public static readonly string BCRYPT_AES_ALGORITHM = "AES";

	public static readonly string MS_PRIMITIVE_PROVIDER = "Microsoft Primitive Provider";

	public static readonly int BCRYPT_AUTH_MODE_CHAIN_CALLS_FLAG = 1;

	public static readonly int BCRYPT_INIT_AUTH_MODE_INFO_VERSION = 1;

	public static readonly uint STATUS_AUTH_TAG_MISMATCH = 3221266434u;

	[DllImport("bcrypt.dll")]
	public static extern uint BCryptOpenAlgorithmProvider(out IntPtr phAlgorithm, [MarshalAs(UnmanagedType.LPWStr)] string pszAlgId, [MarshalAs(UnmanagedType.LPWStr)] string pszImplementation, uint dwFlags);

	[DllImport("bcrypt.dll")]
	public static extern uint BCryptCloseAlgorithmProvider(IntPtr hAlgorithm, uint flags);

	[DllImport("bcrypt.dll")]
	public static extern uint BCryptGetProperty(IntPtr hObject, [MarshalAs(UnmanagedType.LPWStr)] string pszProperty, byte[] pbOutput, int cbOutput, ref int pcbResult, uint flags);

	[DllImport("bcrypt.dll", EntryPoint = "BCryptSetProperty")]
	internal static extern uint BCryptSetAlgorithmProperty(IntPtr hObject, [MarshalAs(UnmanagedType.LPWStr)] string pszProperty, byte[] pbInput, int cbInput, int dwFlags);

	[DllImport("bcrypt.dll")]
	public static extern uint BCryptImportKey(IntPtr hAlgorithm, IntPtr hImportKey, [MarshalAs(UnmanagedType.LPWStr)] string pszBlobType, out IntPtr phKey, IntPtr pbKeyObject, int cbKeyObject, byte[] pbInput, int cbInput, uint dwFlags);

	[DllImport("bcrypt.dll")]
	public static extern uint BCryptDestroyKey(IntPtr hKey);

	[DllImport("bcrypt.dll")]
	public static extern uint BCryptEncrypt(IntPtr hKey, byte[] pbInput, int cbInput, ref pnc8k pPaddingInfo, byte[] pbIV, int cbIV, byte[] pbOutput, int cbOutput, ref int pcbResult, uint dwFlags);

	[DllImport("bcrypt.dll")]
	internal static extern uint BCryptDecrypt(IntPtr hKey, byte[] pbInput, int cbInput, ref pnc8k pPaddingInfo, byte[] pbIV, int cbIV, byte[] pbOutput, int cbOutput, ref int pcbResult, int dwFlags);

	[DllImport("Advapi32")]
	public static extern bool IsTextUnicode(byte[] buf, int len, ref gIo3Gkhe17a opt);
}
