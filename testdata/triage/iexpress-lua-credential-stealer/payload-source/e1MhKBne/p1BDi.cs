using System;
using System.Runtime.InteropServices;
using System.Text;

namespace e1MhKBne;

public static class p1BDi
{
	[DllImport("kernel32.dll", SetLastError = true)]
	public static extern bool CloseHandle(IntPtr hObject);

	[DllImport("kernel32.dll", SetLastError = true)]
	public static extern IntPtr OpenProcess(EKbJ processAccess, bool bInheritHandle, uint processId);

	[DllImport("kernel32.dll", SetLastError = true)]
	public static extern IntPtr GetCurrentProcess();

	[DllImport("kernel32.dll", SetLastError = true)]
	[return: MarshalAs(UnmanagedType.Bool)]
	public static extern bool DuplicateHandle(IntPtr hSourceProcessHandle, IntPtr hSourceHandle, IntPtr hTargetProcessHandle, out IntPtr lpTargetHandle, uint dwDesiredAccess, [MarshalAs(UnmanagedType.Bool)] bool bInheritHandle, _5nh options);

	[DllImport("kernel32.dll")]
	public static extern uint QueryDosDevice(string lpDeviceName, StringBuilder lpTargetPath, uint ucchMax);

	[DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
	public static extern IntPtr CreateFileMapping(IntPtr hFile, IntPtr lpFileMappingAttributes, UR6wXWMpkf flProtect, uint dwMaximumSizeHigh, uint dwMaximumSizeLow, [MarshalAs(UnmanagedType.LPStr)] string lpName);

	[DllImport("kernel32.dll", SetLastError = true)]
	public static extern IntPtr MapViewOfFile(IntPtr hFileMappingObject, ntijC dwDesiredAccess, uint dwFileOffsetHigh, uint dwFileOffsetLow, uint dwNumberOfBytesToMap);

	[DllImport("kernel32.dll", SetLastError = true)]
	public static extern bool UnmapViewOfFile(IntPtr lpBaseAddress);

	[DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
	public static extern IntPtr CreateFile(string FileName, uint DesiredAccess, uint ShareMode, IntPtr SecurityAttributes, uint CreationDisposition, uint FlagsAndAttributes, IntPtr hTemplateFile);

	[DllImport("kernel32.dll", BestFitMapping = true, CharSet = CharSet.Ansi)]
	public static extern bool WriteFile(IntPtr hFile, IntPtr buffer, uint nNumberOfBytesToWrite, out uint lpNumberOfBytesWritten, IntPtr lpOverlapped);

	[DllImport("kernel32.dll")]
	public static extern bool GetFileSizeEx(IntPtr hFile, out long lpFileSize);

	[DllImport("kernel32.dll")]
	public static extern _2xMWq GetFileType(IntPtr hFile);

	[DllImport("kernel32.dll")]
	public static extern uint GetLastError();
}
