using System;
using System.Linq;
using System.Text;
using QUNmAVKTUt;

namespace F3k8m0yephw;

public class w3F6aB : b4mNI9OwAVx
{
	private EmIig _Type;

	private byte[] _Value;

	public EmIig CmmF4 => _Type;

	public ushort TmZ => 0;

	public object It56X1O
	{
		get
		{
			if (_Value == null)
			{
				return null;
			}
			switch (CmmF4)
			{
			case EmIig.VT_I1:
				return (sbyte)_Value[0];
			case EmIig.VT_UI1:
				return _Value[0];
			case EmIig.VT_I2:
				return BitConverter.ToInt16(_Value, 0);
			case EmIig.VT_UI2:
				return BitConverter.ToUInt16(_Value, 0);
			case EmIig.VT_I4:
			case EmIig.VT_INT:
				return BitConverter.ToInt32(_Value, 0);
			case EmIig.VT_ERROR:
			case EmIig.VT_UI4:
			case EmIig.VT_UINT:
				return BitConverter.ToUInt32(_Value, 0);
			case EmIig.VT_I8:
				return BitConverter.ToInt64(_Value, 0);
			case EmIig.VT_CY:
			case EmIig.VT_UI8:
				return BitConverter.ToUInt64(_Value, 0);
			case EmIig.VT_R4:
				return BitConverter.ToSingle(_Value, 0);
			case EmIig.VT_R8:
				return BitConverter.ToDouble(_Value, 0);
			case EmIig.VT_DATE:
			case EmIig.VT_FILETIME:
				return DateTime.FromFileTimeUtc(BitConverter.ToInt64(_Value, 0));
			case EmIig.VT_BOOL:
				return _Value[0] != 0 || _Value[1] != 0;
			case EmIig.VT_LPSTR:
			{
				string text2 = Encoding.Default.GetString(_Value.Skip(4).ToArray());
				char[] trimChars2 = new char[1];
				return text2.TrimEnd(trimChars2);
			}
			case EmIig.VT_LPWSTR:
			{
				string text = Encoding.Unicode.GetString(_Value.Skip(4).ToArray());
				char[] trimChars = new char[1];
				return text.TrimEnd(trimChars);
			}
			case EmIig.VT_CLSID:
				return new Guid(_Value);
			default:
				return _Value;
			}
		}
	}

	public w3F6aB(EmIig Type, byte[] Value)
	{
		_Type = Type;
		_Value = Value;
	}

	public override byte[] GetBytes()
	{
		int num = 0;
		byte[] array = default;
		do
		{
			if (num == 3)
			{
				Buffer.BlockCopy(BitConverter.GetBytes(TmZ), 0, array, 2, 2);
				num = 4;
			}
			if (num == 4)
			{
				if (_Value == null)
				{
					break;
				}
				num = 5;
			}
			if (num == 5)
			{
				Buffer.BlockCopy(_Value, 0, array, 4, _Value.Length);
				num = 6;
			}
			if (num == 1)
			{
				array = new byte[_Value.Length + 4];
				num = 2;
			}
			if (num == 2)
			{
				Buffer.BlockCopy(BitConverter.GetBytes((ushort)CmmF4), 0, array, 0, 2);
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 6);
		return array;
	}

	public override string ToString()
	{
		int num = 0;
		StringBuilder stringBuilder = default;
		do
		{
			if (num == 3)
			{
				stringBuilder.AppendFormat("Type: {0}", CmmF4);
				num = 4;
			}
			if (num == 5)
			{
				stringBuilder.AppendFormat("Value: {0}", It56X1O.ToString());
				num = 6;
			}
			if (num == 6)
			{
				stringBuilder.AppendLine();
				num = 7;
			}
			if (num == 2)
			{
				stringBuilder.Append(base.ToString());
				num = 3;
			}
			if (num == 1)
			{
				stringBuilder = new StringBuilder();
				num = 2;
			}
			if (num == 4)
			{
				stringBuilder.AppendLine();
				num = 5;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 7);
		return stringBuilder.ToString();
	}
}
