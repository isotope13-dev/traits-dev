' Dual-use binary-to-DEBUG script converter (similar to exe2bat / bin2scr).
' Converts a small binary (< 64 KB) into a plain text DOS debug.exe script
' for archival transfer; does not wrap in HTA or execute anything.
Option Explicit
Dim fs, inFile, outScr, f, ts, outStream, hexData, i, addr

Set fs = CreateObject("Scripting.FileSystemObject")
inFile = WScript.Arguments(0)
outScr = WScript.Arguments(1)

Function PairHex(ch)
    Dim s
    s = Hex(AscW(ch))
    Do While Len(s) < 4
        s = "0" & s
    Loop
    PairHex = Right(s, 2) & " " & Left(s, 2) & " "
End Function

Set f = fs.GetFile(inFile)
If f.Size > 65279 Then
    WScript.Echo "Input exceeds 64 KB COM segment limit."
    WScript.Quit 1
End If

Set ts = f.OpenAsTextStream(1, -1)
hexData = ""
Do While Not ts.AtEndOfStream
    hexData = hexData & PairHex(ts.Read(1))
Loop
ts.Close

Set outStream = fs.CreateTextFile(outScr, True)
outStream.WriteLine "n rebuild.com"
For i = 1 To (Len(hexData) \ 48)
    addr = Hex((i - 1) * 16 + 256)
    outStream.WriteLine "e " & addr & " " & Mid(hexData, (i - 1) * 48 + 1, 47)
Next
outStream.WriteLine "rcx"
outStream.WriteLine Hex(f.Size)
outStream.WriteLine "w"
outStream.WriteLine "q"
outStream.Close
