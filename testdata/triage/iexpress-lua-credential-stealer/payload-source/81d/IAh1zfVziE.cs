using System;
using System.Web.Script.Serialization;

namespace _81d;

public class IAh1zfVziE
{
	public string IR1aCl77c<T>(T BmbITjk6P)
	{
		//IL_001f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0028: Expected Obj, but got Unknown
		int num = 0;
		JavaScriptSerializer val = default;
		do
		{
			if (num == 1)
			{
				val = new JavaScriptSerializer();
				num = 2;
			}
			if (num == 2)
			{
				val.MaxJsonLength = int.MaxValue;
				num = 3;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		return val.Serialize((object)BmbITjk6P);
	}

	public T DC91O9qm3Sf<T>(string Icvs)
	{
		//IL_0047: Unknown result type (might be due to invalid IL or missing references)
		//IL_0050: Expected Obj, but got Unknown
		int num = 0;
		JavaScriptSerializer val = default;
		do
		{
			if (num == 2)
			{
				val.MaxJsonLength = int.MaxValue;
				num = 3;
			}
			if (num == 1)
			{
				val = new JavaScriptSerializer();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		return val.Deserialize<T>(Icvs);
	}

	public object bhSExHOp(string l16zDJMToGR, Type LC4)
	{
		//IL_0047: Unknown result type (might be due to invalid IL or missing references)
		//IL_0050: Expected Obj, but got Unknown
		int num = 0;
		JavaScriptSerializer val = default;
		do
		{
			if (num == 2)
			{
				val.MaxJsonLength = int.MaxValue;
				num = 3;
			}
			if (num == 1)
			{
				val = new JavaScriptSerializer();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		return val.Deserialize(l16zDJMToGR, LC4);
	}
}
