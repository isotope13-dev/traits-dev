using System;

namespace e1MhKBne;

[Flags]
public enum ntijC : uint
{
	FileMapCopy = 1u,
	FileMapWrite = 2u,
	FileMapRead = 4u,
	FileMapAllAccess = 0x1Fu,
	FileMapExecute = 0x20u
}
